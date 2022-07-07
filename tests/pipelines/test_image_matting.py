# Copyright (c) Alibaba, Inc. and its affiliates.
import os.path as osp
import tempfile
import unittest

import cv2

from modelscope.fileio import File
from modelscope.msdatasets import MsDataset
from modelscope.pipelines import pipeline
from modelscope.pipelines.outputs import OutputKeys
from modelscope.utils.constant import ModelFile, Tasks
from modelscope.utils.test_utils import test_level


class ImageMattingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.model_id = 'damo/cv_unet_image-matting'

    @unittest.skip('deprecated, download model from model hub instead')
    def test_run_with_direct_file_download(self):
        model_path = 'http://pai-vision-data-hz.oss-cn-zhangjiakou.aliyuncs' \
                     '.com/data/test/maas/image_matting/matting_person.pb'
        with tempfile.TemporaryDirectory() as tmp_dir:
            model_file = osp.join(tmp_dir, ModelFile.TF_GRAPH_FILE)
            with open(model_file, 'wb') as ofile:
                ofile.write(File.read(model_path))
            img_matting = pipeline(Tasks.image_matting, model=tmp_dir)

            result = img_matting('data/test/images/image_matting.png')
            cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_run_with_dataset(self):
        input_location = ['data/test/images/image_matting.png']
        # alternatively:
        # input_location = '/dir/to/images'

        dataset = MsDataset.load(input_location, target='image')
        img_matting = pipeline(Tasks.image_matting, model=self.model_id)
        # note that for dataset output, the inference-output is a Generator that can be iterated.
        result = img_matting(dataset)
        cv2.imwrite('result.png', next(result)[OutputKeys.OUTPUT_IMG])
        print(f'Output written to {osp.abspath("result.png")}')

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_run_modelhub(self):
        img_matting = pipeline(
            Tasks.image_matting, model=self.model_id, model_revision='beta')

        result = img_matting('data/test/images/image_matting.png')
        cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])
        print(f'Output written to {osp.abspath("result.png")}')

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_modelhub_default_model(self):
        img_matting = pipeline(Tasks.image_matting)

        result = img_matting('data/test/images/image_matting.png')
        cv2.imwrite('result.png', result[OutputKeys.OUTPUT_IMG])
        print(f'Output written to {osp.abspath("result.png")}')

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_with_modelscope_dataset(self):
        dataset = MsDataset.load(
            'beans', namespace='damotest', split='train', target='image')
        img_matting = pipeline(Tasks.image_matting, model=self.model_id)
        result = img_matting(dataset)
        for i in range(10):
            cv2.imwrite(f'result_{i}.png', next(result)[OutputKeys.OUTPUT_IMG])
        print(
            f'Output written to dir: {osp.dirname(osp.abspath("result_0.png"))}'
        )


if __name__ == '__main__':
    unittest.main()
