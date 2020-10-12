import tensorflow as tf
import tensorflow.keras as ks
from typing import *

import yolo.modeling.base_model as base_model
from yolo.modeling.backbones.backbone_builder import Backbone_Builder
from yolo.modeling.model_heads._Yolov3Head import Yolov3Head
from yolo.modeling.building_blocks import YoloLayer

from yolo.utils.file_manager import download
from yolo.utils import DarkNetConverter
from yolo.utils._darknet2tf.load_weights import split_converter, load_weights_dnBackbone, load_weights_dnHead


class Yolov1(base_model.Yolo):
    def __init__(
            self,
            input_shape=[None, None, None, 3],
            model="yolov1",  # options {regular, spp, tiny}
            classes=80,
            backbone=None,
            head=None,
            head_filter=None,
            masks=None,
            boxes=None,
            path_scales=None,
            x_y_scales=None,
            thresh: int = 0.45,
            class_thresh: int = 0.45,
            max_boxes: int = 200,
            scale_boxes: int = 416,
            scale_mult: float = 1.0,
            use_tie_breaker: bool = False,
            clip_grads_norm = None,
            policy="float32",
            **kwargs):
        super().__init__(**kwargs)

        #required inputs
        self._input_shape = input_shape
        self._classes = classes
        self._type = model
        self._encoder_decoder_split_location = None
        self._built = False
        self._custom_aspects = False

        #setting the running policy
        if type(policy) != str:
            policy = policy.name
        self._og_policy = policy
        self._policy = tf.keras.mixed_precision.experimental.global_policy(
        ).name
        self.set_policy(policy=policy)

        #filtering params
        self._thresh = thresh
        self._class_thresh = 0.45
        self._max_boxes = max_boxes
        self._scale_boxes = scale_boxes
        self._scale_mult = scale_mult
        self._x_y_scales = x_y_scales

        #init base params
        self._encoder_decoder_split_location = None
        self._boxes = boxes
        self._masks = masks
        self._path_scales = path_scales
        self._use_tie_breaker = use_tie_breaker

        #init models
        self.model_name = model
        self._model_name = None
        self._backbone_name = None
        self.backbone = backbone
        self.head = head
        self.head_filter = head_filter

        self._clip_grads_norm = clip_grads_norm

        self.get_models()
        return

    def get_models(self):
        default_dict = {
            "regular": {
                "backbone": "darknet53",
                "head": "regular",
                "name": "yolov3"
            },
            "spp": {
                "backbone": "darknet53",
                "head": "spp",
                "name": "yolov3-spp"
            },
            "tiny": {
                "backbone": "darknet_tiny",
                "head": "tiny",
                "name": "yolov3-tiny"
            },
            "yolov1": {
                "backbone": "yolov1_backbone"
            }
        }

        if self.model_name == "regular" or self.model_name == "spp":
            self._encoder_decoder_split_location = 76
            self._boxes = self._boxes or [(10, 13), (16, 30), (33, 23),
                                          (30, 61), (62, 45), (59, 119),
                                          (116, 90), (156, 198), (373, 326)]
            self._masks = self._masks or {
                "1024": [6, 7, 8],
                "512": [3, 4, 5],
                "256": [0, 1, 2]
            }
            self._path_scales = self._path_scales or {
                "1024": 32,
                "512": 16,
                "256": 8
            }
            self._x_y_scales = self._x_y_scales or {
                "1024": 1.0,
                "512": 1.0,
                "256": 1.0
            }
        elif self.model_name == "tiny":
            self._encoder_decoder_split_location = 14
            self._boxes = self._boxes or [(10, 14), (23, 27), (37, 58),
                                          (81, 82), (135, 169), (344, 319)]
            self._masks = self._masks or {"1024": [3, 4, 5], "256": [0, 1, 2]}
            self._path_scales = self._path_scales or {"1024": 32, "256": 8}
            self._x_y_scales = self._x_y_scales or {"1024": 1.0, "256": 1.0}

        if self.backbone == None or isinstance(self.backbone, Dict):
            self._backbone_name = default_dict[self.model_name]["backbone"]
            if isinstance(self.backbone, Dict):
                default_dict[self.model_name]["backbone"] = self.backbone
            self.backbone = Backbone_Builder(
                name=default_dict[self.model_name]["backbone"],
                config=default_dict[self.model_name]["backbone"],
                input_shape=self._input_shape)

        else:
            self._custom_aspects = True

        if self.head == None or isinstance(self.head, Dict):
            if isinstance(self.head, Dict):
                default_dict[self.model_name]["head"] = self.head
            self.head = Yolov3Head(
                model=default_dict[self.model_name]["head"],
                cfg_dict=default_dict[self.model_name]["head"],
                classes=self._classes,
                boxes=len(self._boxes),
                input_shape=self._input_shape)
        else:
            self._custom_aspects = True

        if self.head_filter == None:
            self.head_filter = YoloLayer(masks=self._masks,
                                         anchors=self._boxes,
                                         thresh=self._thresh,
                                         cls_thresh=self._class_thresh,
                                         max_boxes=self._max_boxes,
                                         scale_boxes=self._scale_boxes,
                                         scale_mult=self._scale_mult,
                                         path_scale=self._path_scales)

        self._model_name = default_dict[self.model_name]["name"]
        return

    def get_summary(self):
        self.backbone.summary()
        self.head.summary()
        print(self.backbone.output_shape)
        print(self.head.output_shape)
        return

    def build(self, input_shape):
        self.backbone.build(input_shape)
        self.head.build(self.backbone.output_shape)
        self.head_filter.build(self.head.output_shape)
        return

    def call(self, inputs, training=True):
        feature_maps = self.backbone(inputs)
        raw_head = self.head(feature_maps)
        predictions = self.head_filter(raw_head)
        return predictions

    def load_weights_from_dn(self,
                             dn2tf_backbone=True,
                             dn2tf_head=True,
                             config_file=None,
                             weights_file=None):
        """
        load the entire Yolov3 Model for tensorflow

        example:
            load yolo with darknet wieghts for backbone
            model = Yolov3()
            model.build(input_shape = (1, 416, 416, 3))
            model.load_weights_from_dn(dn2tf_backbone = True, dn2tf_head = True)

        to be implemented
        example:
            load custom back bone weigths

        example:
            load custom head weigths

        example:
            load back bone weigths from tensorflow (our training)

        example:
            load head weigths from tensorflow (our training)

        Args:
            dn2tf_backbone: bool, if true it will load backbone weights for yolo v3 from darknet .weights file
            dn2tf_head: bool, if true it will load head weights for yolo v3 from darknet .weights file
            config_file: str path for the location of the configuration file to use when decoding darknet weights
            weights_file: str path with the file containing the dark net weights
        """
        if dn2tf_backbone or dn2tf_head:
            if config_file is None:
                config_file = download(self._model_name + '.cfg')
            if weights_file is None:
                weights_file = download(self._model_name + '.weights')
            list_encdec = DarkNetConverter.read(config_file, weights_file)
            encoder, decoder = split_converter(
                list_encdec, self._encoder_decoder_split_location)

        if dn2tf_backbone:
            load_weights_dnBackbone(self.backbone,
                                    encoder,
                                    mtype=self._backbone_name)

        if dn2tf_head:
            load_weights_dnHead(self.head, decoder)
        return


if __name__ == "__main__":
    model = Yolov1(model = "yolov1", policy="mixed_float16")