"""Intersection over union calculation utils."""

# Import libraries
import tensorflow as tf
import math

from yolo.utils.box_utils import _xcycwh_to_xyxy
from yolo.utils.box_utils import _xcycwh_to_yxyx
from yolo.utils.box_utils import _yxyx_to_xcycwh
from yolo.utils.box_utils import _get_area
from yolo.utils.box_utils import _intersection_and_union
from yolo.utils.box_utils import _aspect_ratio_consistancy
from yolo.utils.box_utils import _center_distance


def compute_iou(box1, box2):
    """Calculates the intersection of union between box1 and box2.
    Args:
        box1: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
        box2: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
    Returns:
        iou: a `Tensor` who represents the intersection over union.
    """
    # get box corners
    with tf.name_scope("iou"):
        box1 = _xcycwh_to_xyxy(box1)
        box2 = _xcycwh_to_xyxy(box2)
        intersection, union = _intersection_and_union(box1, box2)

        iou = tf.math.divide_no_nan(intersection, union)
        iou = tf.clip_by_value(iou, clip_value_min=0.0, clip_value_max=1.0)
    return iou


def compute_giou(box1, box2):
    """Calculates the generalized intersection of union between box1 and box2.
    Args:
        box1: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
        box2: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
    Returns:
        iou: a `Tensor` who represents the generalized intersection over union.
    """
    with tf.name_scope("giou"):
        # get box corners
        box1 = _xcycwh_to_xyxy(box1)
        box2 = _xcycwh_to_xyxy(box2)

        # compute IOU
        intersection, union = _intersection_and_union(box1, box2)
        iou = tf.math.divide_no_nan(intersection, union)
        iou = tf.clip_by_value(iou, clip_value_min=0.0, clip_value_max=1.0)

        # find the smallest box to encompase both box1 and box2
        c_mins = tf.math.minimum(box1[..., 0:2], box2[..., 0:2])
        c_maxes = tf.math.maximum(box1[..., 2:4], box2[..., 2:4])
        c = _get_area((c_mins, c_maxes), use_tuple=True)

        # compute giou
        giou = iou - tf.math.divide_no_nan((c - union), c)
    return iou, giou


def compute_diou(box1, box2):
    """Calculates the distance intersection of union between box1 and box2.
    Args:
        box1: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
        box2: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
    Returns:
        iou: a `Tensor` who represents the distance intersection over union.
    """
    with tf.name_scope("diou"):
        # compute center distance
        dist = _center_distance(box1[..., 0:2], box2[..., 0:2])

        # get box corners
        box1 = _xcycwh_to_xyxy(box1)
        box2 = _xcycwh_to_xyxy(box2)

        # compute IOU
        intersection, union = _intersection_and_union(box1, box2)
        iou = tf.math.divide_no_nan(intersection, union)
        iou = tf.clip_by_value(iou, clip_value_min=0.0, clip_value_max=1.0)

        # compute max diagnal of the smallest enclosing box
        c_mins = tf.math.minimum(box1[..., 0:2], box2[..., 0:2])
        c_maxes = tf.math.maximum(box1[..., 2:4], box2[..., 2:4])
        diag_dist = _center_distance(c_mins, c_maxes)

        regularization = tf.math.divide_no_nan(dist, diag_dist)
        diou = iou + regularization
    return iou, diou


def compute_ciou(box1, box2):
    """Calculates the complete intersection of union between box1 and box2.
    Args:
        box1: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
        box2: a `Tensor` whose last dimension is 4 representing the coordinates of boxes in
            x_center, y_center, width, height.
    Returns:
        iou: a `Tensor` who represents the complete intersection over union.
    """
    with tf.name_scope("ciou"):
        #compute DIOU and IOU
        iou, diou = compute_diou(box1, box2)

        # computer aspect ratio consistency
        v = _aspect_ratio_consistancy(box1[..., 2], box1[..., 3], box2[..., 2],
                                      box2[..., 3])

        # compute IOU regularization
        a = tf.math.divide_no_nan(v, ((1 - iou) + v))
        ciou = diou + v * a
    return iou, ciou