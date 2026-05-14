from .load_image_url_node import LoadImageByUrl
from .Image2Oss import OSSUploadNode, OSSUploadNodeBySTSServiceUrl
from .Image2Oss import LoadImageFromURL, LoadImageFromOss, LoadImageFromOssBySTSServiceUrl

NODE_CLASS_MAPPINGS = {
    "AC_从URL加载图像":LoadImageByUrl,
    "AC_Oss上传图像":OSSUploadNode,
    "AC_Oss上传服务":OSSUploadNodeBySTSServiceUrl,
    "AC_从URL加载图像":LoadImageFromURL,
    "AC_从Oss加载图像":LoadImageFromOss,
    "AC_从Oss加载图像(使用服务)":LoadImageFromOssBySTSServiceUrl
}
