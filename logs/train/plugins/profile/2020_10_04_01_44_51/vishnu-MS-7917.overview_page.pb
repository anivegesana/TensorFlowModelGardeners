�&$	�2e@�
M$@��	m9�?!��g��@@	��o��@U�fm�m0@!��y�!>K@"n
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails-��g��@@˼Uס��?1|a2U0**@I��-�/�?Y��O#2@"^
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails�UH�IM"@1��I���r?I���a�J"@"^
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails����`�?1s�,&6�?I�����?"^
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetailsB��^~��?1˻��?Ih����[�?"^
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails*���;�?1��n/i��?I31]�տ?"^
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails"6X8I��?1_����?I��d���?"g
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails&`��ME*�?K�P��?1j�����?I�#~�.�?"g
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails&�pvk��?*T7�C?1�+����?I���t�?"g
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails&�Rz���?7�n�e�?1V�F�?�?I`���~��?"g
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails&	g`�eM,�?��N^�?1*��g\8�?I�&�5��?"g
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails&
��	m9�?[�[!��b?13���/�?I���8��?*1�Zd_@��n;��@2K
Iterator::Model::Map!<�8b]4@!U��+ľX@)���e�%@1Gf��'J@:Preprocessing2_
(Iterator::Model::Map::PaddedBatchV2::Map��֦�@!�xag¦A@)�W<�H@1)yo�A@:Preprocessing2Z
#Iterator::Model::Map::PaddedBatchV2#��^4#@!�����UG@)�ơ~�@1X� �l�&@:Preprocessing2�
�Iterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2::ParallelMapV2::AssertCardinality::ParallelInterleaveV4[0]::FlatMap[0]::TFRecord�I����?!R��
���?)�I����?1R��
���?:Advanced file read2�
yIterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2::ParallelMapV2::AssertCardinality::ParallelInterleaveV4�Nt�?!��m����?)�Nt�?1��m����?:Preprocessing2�
cIterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2::ParallelMapV2::AssertCardinality��qn�?!P��j���?)+��	h�?1푉L�]�?:Preprocessing2�
�Iterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2::ParallelMapV2::AssertCardinality::ParallelInterleaveV4[0]::FlatMapc_��`��?!
�:�uQ�?)�X�oC��?1~ғ윬?:Preprocessing2�
PIterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2::ParallelMapV2�{�Y�H�?!��H�J�?)�{�Y�H�?1��H�J�?:Preprocessing2x
AIterator::Model::Map::PaddedBatchV2::Map::Prefetch::ParallelMapV2��vL݅?!WӝB��?)��vL݅?1WӝB��?:Preprocessing2i
2Iterator::Model::Map::PaddedBatchV2::Map::Prefetch���4cф?!����K�?)���4cф?1����K�?:Preprocessing2F
Iterator::Model�0DN__4@!e9��.�X@)I�V�?1�z
�T�?:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
host�Your program is HIGHLY input-bound because 40.2% of the total step time sampled is waiting for input. Therefore, you should first focus on reducing the input time.high"�29.0 % of the total step time sampled is spent on 'Kernel Launch'. It could be due to CPU contention with tf.data. In this case, you may try to set the environment variable TF_GPU_THREAD_MODE=gpu_private.*no9
���D@>Look at Section 3 for the breakdown of input time on the host.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	7J�Q���?������?!˼Uס��?	!       "$	�m���?5'�N�j@��I���r?!|a2U0**@*	!       2	!       :$	P|>`��?�%l�@���8��?!���a�J"@B	!       J	}�n��a�?(]���@!��O#2@R	!       Z	}�n��a�?(]���@!��O#2@JGPUY
���D@b �
"�
_gradient_tape/yolov4/neck/dark_route_process/dark_conv_72/conv2d_73/Conv2D/Conv2DBackpropFilterConv2DBackpropFilter媛��@�?!媛��@�?"S
:yolov4/darknet53/DarkRes_2_csp_down/dark_conv_9/mish_9/mulMul5��g�?!"��(�?"�
egradient_tape/yolov4/regular/dark_route_process_4/dark_conv_99/conv2d_108/Conv2D/Conv2DBackpropFilterConv2DBackpropFilterx}��?!�p����?"�
_gradient_tape/yolov4/neck/dark_route_process/dark_conv_75/conv2d_76/Conv2D/Conv2DBackpropFilterConv2DBackpropFilter�Uu�Mp�?!S��[	л?"�
egradient_tape/yolov4/regular/dark_route_process_4/dark_conv_97/conv2d_106/Conv2D/Conv2DBackpropFilterConv2DBackpropFilter
����m�?!+�$�U�?"�
egradient_tape/yolov4/regular/dark_route_process_4/dark_conv_95/conv2d_104/Conv2D/Conv2DBackpropFilterConv2DBackpropFilter�55��6�?!�ř���?"^
Byolov4/regular/dark_route_process_4/dark_conv_97/conv2d_106/Conv2DConv2D0�mAq��?!���>�q�?"�
dgradient_tape/yolov4/regular/dark_route_process_4/dark_conv_97/conv2d_106/Conv2D/Conv2DBackpropInputConv2DBackpropInput R�G���?!�9A3���?"^
Byolov4/regular/dark_route_process_4/dark_conv_99/conv2d_108/Conv2DConv2D����KA�?!Z?��^�?"�
dgradient_tape/yolov4/regular/dark_route_process_4/dark_conv_99/conv2d_108/Conv2D/Conv2DBackpropInputConv2DBackpropInputu���&(�?!q,�\e��?Q      Y@Yq��]q�4@ad��c�S@q/R�� @y��mJrH�?"�

host�Your program is HIGHLY input-bound because 40.2% of the total step time sampled is waiting for input. Therefore, you should first focus on reducing the input time.b
`input_pipeline_analyzer (especially Section 3 for the breakdown of input operations on the Host)m
ktrace_viewer (look at the activities on the timeline of each Host Thread near the bottom of the trace view)"O
Mtensorflow_stats (identify the time-consuming operations executed on the GPU)"U
Strace_viewer (look at the activities on the timeline of each GPU in the trace view)*�
�<a href="https://www.tensorflow.org/guide/data_performance_analysis" target="_blank">Analyze tf.data performance with the TF Profiler</a>*y
w<a href="https://www.tensorflow.org/guide/data_performance" target="_blank">Better performance with the tf.data API</a>2�
=type.googleapis.com/tensorflow.profiler.GenericRecommendation�
high�29.0 % of the total step time sampled is spent on 'Kernel Launch'. It could be due to CPU contention with tf.data. In this case, you may try to set the environment variable TF_GPU_THREAD_MODE=gpu_private.no*�Only 0.0% of device computation is 16 bit. So you might want to replace more 32-bit Ops by 16-bit Ops to improve performance (if the reduced accuracy is acceptable).:
Refer to the TF2 Profiler FAQ2"GPU(: B 