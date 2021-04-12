import torch
from PIL import Image
from torchvision import transforms
from pix2pixHD.data.base_dataset import __scale_width
from pix2pixHD.models.networks import define_G
import pix2pixHD.util.util as util
from aligner import align_face
import dlib
import imageio
import random


config_G = {
        'input_nc': 3,
        'output_nc': 3,
        'ngf': 64,
        'netG': 'global',
        'n_downsample_global': 4,
        'n_blocks_global': 9,
        'n_local_enhancers': 1,
        'norm': 'instance',
    }


def init_model(config, weights_path):
    model = define_G(**config)
    pretrained_dict = torch.load(weights_path)
    model.load_state_dict(pretrained_dict)
    return model


def get_eval_transform(load_size=512):
    transform_list = [transforms.Lambda(lambda img: __scale_width(img,
                                                                  load_size,
                                                                  Image.BICUBIC))]
    transform_list += [transforms.ToTensor()]
    transform_list += [transforms.Normalize((0.5, 0.5, 0.5),
                                            (0.5, 0.5, 0.5))]
    return transforms.Compose(transform_list)


model_to_male = init_model(config_G, 'model_weights/to_male_net_G.pth')
model_to_female = init_model(config_G, 'model_weights/to_female_net_G.pth')
shape_predictor = dlib.shape_predictor('model_weights/landmarks.dat')


def swap_gender(img_bytes):
    """
    Get predictions (swaps gender on image for both cases - male and female)
    from pretrained model
    Args:
        img_bytes: type(bytes) the image file in bytes read by Python

    Returns: type(list) sequence of 2 result filenames. Images are saved into static folder.

    """
    aligned_img = align_face(img_bytes, shape_predictor)[0]
    transform = get_eval_transform()
    img = transform(aligned_img).unsqueeze(0)

    results = []
    for model, res_name in zip([model_to_male, model_to_female],
                               ['to_male', 'to_female']):
        with torch.no_grad():
            output = model(img)

        output = util.tensor2im(output.data[0])
        # res_filename = f"predictions/{model_weight.split('/')[1][:-4]}_result_{random.randrange(100000)}.jpg"
        res_filename = f"static/{res_name}_result_{random.randrange(100000)}.jpg"
        results.append(res_filename)

        imageio.imsave(res_filename, output)

    return results
