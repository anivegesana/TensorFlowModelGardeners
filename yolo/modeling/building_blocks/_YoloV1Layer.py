import tensorflow as tf
import tensorflow.keras as ks

from yolo.utils.box_utils import _xcycwh_to_yxyx
from yolo.utils.loss_utils import _build_grid_points

#@ks.utils.register_keras_serializable(package='yolo_v1')
class YoloV1Layer(ks.Model):
    def __init__(self, 
                 num_boxes,
                 num_classes,
                 size,
                 img_size,
                 thresh,
                 cls_thresh,
                 use_nms=True,
                 **kwargs):
        """
        Detection layer for YOLO v1
        Args: 
            num_boxes: integer, number of prediction boxes per grid cell 
            num_classes: integer, number of class probabilities each box predicts
            size: integer, specifying that the input has size * size grid cells
            img_size: integer, pixel height/width of the input image
            thresh: float, iou threshold used for non-max-supression
            cls_thresh: float, score threshold used for non-max-suppression
            use_nms: bool, True for filtering boxes using non-max-suppression
        call Return: 
            dict: with keys "bbox", "classes", "confidence", and "raw_output" 
        """
        super().__init__(**kwargs)
        self._num_boxes = num_boxes
        self._num_classes = num_classes
        self._size = size
        self._img_size = img_size

        self._thresh = thresh
        self._cls_thresh = cls_thresh
        self._use_nms = use_nms 

        self._max_boxes = self._size * self._size * self._num_boxes
    
    def parse_boxes(self, boxes):
        """
        Parameterizes xywh boxes coordinates by absolute location within [0, 1]
        Args:
            boxes: tensor of shape [batches, size, size, num_boxes, 4]
        Returns:
            Tensor: shape [batches, size * size * num_boxes, 4]
        """
        grid_points = _build_grid_points(self._size, self._size, self._num_boxes, dtype=tf.float32)

        boxes_xy = boxes[...,0:2]
        #boxes_xy = tf.math.sigmoid(boxes_xy)

        boxes_wh = boxes[...,2:4]
        boxes_wh = tf.math.pow(boxes_wh, 2) # from src code

        boxes_xy =tf.stack([boxes_xy[..., 0]/self._size, boxes_xy[..., 1]/self._size], axis=-1) + grid_points
        boxes = tf.concat([boxes_xy, boxes_wh], axis=-1)
        return boxes

    def parse_prediction(self, inputs):
        """
        Parses a prediction tensor into its box, class, and confidence components
        Args:
            inputs: tensor of shape [batches, size, size, boxes * 5 + classes]

        Return:
            boxes coordinates, classes predictions, for
            each bounding box prediction 
        """

        # Seperate bounding box components from class probabilities:
        class_start = self._num_boxes * 5
        boxes_xywhc = inputs[..., :class_start]
        classes = inputs[..., class_start:]

        # Get components from boxes:
        boxes_xywhc = tf.reshape(boxes_xywhc, [-1, self._size, self._size, self._num_boxes, 5])
        confidence = boxes_xywhc[..., 4]
        boxes_xywh = boxes_xywhc[..., :4]
        
        # Process boxes for nms
        boxes_xywh = self.parse_boxes(boxes_xywh)
        boxes_yxyx = _xcycwh_to_yxyx(boxes_xywh)
        boxes_yxyx = tf.reshape(boxes_yxyx, [-1, self._max_boxes, 4])
        boxes_yxyx = tf.expand_dims(boxes_yxyx, axis=2)

        # Process box scores for nms
        #classes = tf.math.sigmoid(classes)
        classes = ks.activations.softmax(classes, axis=-1)
        confidence = tf.math.sigmoid(confidence)

        classes = tf.stack([classes] * self._num_boxes, axis=-2)
        confidence = tf.expand_dims(confidence, axis=-1)
        classes = classes * confidence

        classes = tf.reshape(classes, [-1, self._max_boxes, self._num_classes])

        return boxes_yxyx, classes


    def call(self, inputs):
        """
        Parses a prediction tensor into its box, class, and confidence components
        Args:
            inputs: output from the detection head (7x7x35)

        Return:
            dict: Dictionary with keys "bbox", "classes", "confidence", and "raw_output"
            bbox: tensor with the yxyx coordinates of each box (coordinates normalized between 0 and 1)
            classes: number, one-hot encoding of the predicted class
            confidence: predicted confidence of an object existing in the grid cell
            raw_output: size x size x (numBoxes * 5 + numClasses) tensor
        """
        boxes, classes = self.parse_prediction(inputs)

        if self._use_nms:
            boxes = tf.cast(boxes, tf.float32)
            classes = tf.cast(classes, tf.float32)

            # boxes and classes are already in correct shape
            nms = tf.image.combined_non_max_suppression(
                boxes, classes, self._max_boxes,
                self._max_boxes, self._thresh, self._cls_thresh)
            
            return {
                "bbox": nms.nmsed_boxes,
                "classes": nms.nmsed_classes,
                "confidence": nms.nmsed_scores,
                "raw_output": inputs
            }
        else:
            return {
                "bbox": boxes,
                "classes": tf.math.argmax(classes, axis=-1),
                "confidence": classes,
                "raw_output": inputs
            }


if __name__ == "__main__":
    num_boxes = 3
    num_classes = 20
    size = 7
    thresh = 0.45
    cls_thresh = 0.45
    img_dims = 448

    input_size = size * size * (num_boxes * 5 + num_classes)
    random_input = tf.random.uniform(shape=(2, size, size, num_boxes * 5 + num_classes), maxval=1, dtype=tf.float32)

    print("Testing yolo layer:")
    yolo_layer = YoloV1Layer(num_boxes=num_boxes,
                             num_classes=num_classes,
                             size=size,
                             img_size=img_dims,
                             thresh=thresh,
                             cls_thresh=cls_thresh,
                             use_nms=True)
    
    output = yolo_layer(random_input)
    print(output['classes'])
    print(output['confidence'])
    print(output['bbox'])