import tensorflow as tf
import tensorflow.keras as ks
from typing import *

import yolo.modeling.base_model as base_model
from yolo.modeling.backbones.backbone_builder import Backbone_Builder
from yolo.modeling.model_heads._Yolov1Head import Yolov1Head
from yolo.modeling.building_blocks import YoloLayer

from yolo.utils.file_manager import download
from yolo.utils import DarkNetConverter
from yolo.utils._darknet2tf.load_weights import split_converter, load_weights_dnBackbone, load_weights_dnHead

class Yolov1(base_model.Yolo):
    def __init__(
            self,
            input_shape=[None, None, None, 3],
            model="regular",  # options {regular, spp, tiny}
            classes=20,
            backbone=None,
            head=None,
            head_filter=None,
            masks=None,
            boxes=2,
            path_scales=None,
            x_y_scales=None,
            thresh: int = 0.45,
            weight_decay = 5e-4, 
            class_thresh: int = 0.45,
            use_nms = True,
            using_rt = False,
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
        self._backbone_cfg = backbone
        self._head_cfg = head
        self._head_filter_cfg = head_filter
        self._weight_decay = weight_decay
        self._use_nms = use_nms
        self._using_rt = using_rt

        self._clip_grads_norm = clip_grads_norm

        self.get_default_attributes()
        self._loss_fn = None
        self._loss_weight = None
        return

    def get_default_attributes(self):
        pass

    def get_summary(self):
        self._backbone.summary()
        self._head.summary()
        print(self._backbone.output_shape)
        print(self._head.output_shape)
        self.summary()
        return

    def build(self, input_shape):
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
                "backbone": "yolov1_backbone",
                "head": "regular",
                "name": "yolov1"
            }
        }
        if self._backbone_cfg == None or isinstance(self._backbone_cfg, Dict):
            self._backbone_name = default_dict[self.model_name]["backbone"]
            if isinstance(self._backbone_cfg, Dict):
                default_dict[self.model_name]["backbone"] = self._backbone_cfg
            self._backbone = Backbone_Builder(
                name=default_dict[self.model_name]["backbone"],
                config=default_dict[self.model_name]["backbone"],
                input_shape=self._input_shape, 
                weight_decay=self._weight_decay)
        else:
            self._backbone = self._backbone_cfg
            self._custom_aspects = True
        
        if self._head_cfg == None or isinstance(self._head_cfg, Dict):
            if isinstance(self._head_cfg, Dict):
                default_dict[self.model_name]["head"] = self._head_cfg
            self._head = Yolov1Head(
                model=default_dict[self.model_name]["head"],
                config=default_dict[self.model_name]["head"],
                classes=self._classes,
                boxes=self._boxes,
                input_shape=self._input_shape)
        else:
            self._head = self._head_cfg
            self._custom_aspects = True

        self._model_name = default_dict[self.model_name]["name"]
        self._backbone.build(input_shape)
        self._head.build(self._backbone.output_shape)
        self._built = True
        super().build(input_shape)
        return

    def call(self, inputs, training=False):
        feature_maps = self._backbone(inputs)
        raw_head = self._head(feature_maps)
        if training or self._using_rt:
            return {"raw_output": raw_head}
        else:
            predictions = self._head_filter(raw_head)
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
        if not self._built:
            self.build(self._input_shape)

        if dn2tf_backbone or dn2tf_head:
            if config_file is None:
                config_file = download(self._model_name + '.cfg')
            if weights_file is None:
                weights_file = download(self._model_name + '.weights')
            list_encdec = DarkNetConverter.read(config_file, weights_file)
            encoder, decoder = split_converter(
                list_encdec, self._encoder_decoder_split_location)

        if dn2tf_backbone:
            load_weights_dnBackbone(self._backbone,
                                    encoder,
                                    mtype=self._backbone_name)

        if dn2tf_head:
            load_weights_dnHead(self._head, decoder)
        return
if __name__ == "__main__":
    model = Yolov1(model = "yolov1")
    model.build((1, 448, 448, 3))