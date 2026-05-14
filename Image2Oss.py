from .util import tensor_to_pil,read_image_from_url,put_object,get_aliyun_ak,OSS_ENDPOINT_LIST,get_object
# from comfy.cli_args import args
import ast
from .category import Ac

class OSSUploadNode(Ac):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filename": ("STRING",{"default":'["tmp-comfyui/filename.png"]'}),
                "access_key_id": ("STRING", {"default": "access_key_id"}),
                "access_key_secret": ("STRING", {"default": "access_key_secret"}),
                "security_token": ("STRING", {"default": ""}),
                "bucket_name": ("STRING", {"default": "bucket_name"}),
                "endpoint": (OSS_ENDPOINT_LIST,{"default": "oss-cn-shenzhen.aliyuncs.com"}),
            }
        }

    # 校验参数是否正确
    @classmethod
    def VALIDATE_INPUTS(cls,image, filename, access_key_id, access_key_secret, bucket_name, endpoint):
        #print("参数校验:\t%s,%s,%s,%s,%s" % (filename, access_key_id, access_key_secret, bucket_name, endpoint))
        if filename == "" or access_key_id == "" or access_key_secret == "" or bucket_name == "" or endpoint == "":
            return "参数不能为空"
        # 检查endpoing
        if endpoint not in OSS_ENDPOINT_LIST:
            return "endpoint 不正确\t %s" % endpoint
        return True
    RETURN_TYPES = ()
    FUNCTION = "upload_to_oss"
    OUTPUT_NODE = True
    def upload_to_oss(self, image, filename, access_key_id, access_key_secret,security_token, bucket_name, endpoint):
        #print("参数信息: \t%s,%s,%s,%s,%s\n" %( filename,access_key_id, access_key_secret, bucket_name, endpoint))

        # 先判断这里是不是字符串
        if not isinstance(filename, str):
            raise ValueError("文件名必须为列表")
        try:
            filenameList = ast.literal_eval(filename)
            if isinstance(filenameList, list):  # 检查解析后的结果是否是列表
                pass
            else:
                raise ValueError("文件名必须为列表")
        except:
            raise ValueError("文件名必须为列表")
        print("共有图片[%s]张,filename[%s]个\n" % (len(image), len(filenameList) ))
        if len(image)!= len(filenameList) :
            raise ValueError("生成图片数量与给定的文件名数量不对应")
        n = 0
        for i in image:
            img = tensor_to_pil(i)
            #print("文件名称: [%s] \t文件类型: %s" % (filenameList[n],type(img)))
            put_object(img,filenameList[n],access_key_id, access_key_secret, security_token,bucket_name, endpoint)
            n = n + 1

        return ()



class OSSUploadNodeBySTSServiceUrl(Ac):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filename": ("STRING",{"default":'["tmp-comfyui/filename.png"]'}),
                "sts_service_url": ("STRING", {"default": "https://demo.cn/sts_service"}),
                "bucket_name": ("STRING", {"default": "bucket_name"}),
                "endpoint": (OSS_ENDPOINT_LIST,{"default": "oss-cn-shenzhen.aliyuncs.com"}),
            }
        }
        # 校验参数是否正确
    @classmethod
    def VALIDATE_INPUTS(cls,image, filename, sts_service_url, bucket_name, endpoint):
        if filename == "" or sts_service_url == "" or bucket_name == "" or endpoint == "":
            return "参数不能为空"
        # 检查endpoing
        if endpoint not in OSS_ENDPOINT_LIST:
            return "endpoint 不正确\t %s" % endpoint
        return True
    RETURN_TYPES = ()
    FUNCTION = "upload_to_oss"
    OUTPUT_NODE = True
    def upload_to_oss(self, image, filename, sts_service_url, bucket_name, endpoint):
        # 先判断这里是不是字符串
        if not isinstance(filename, str):
            raise ValueError("文件名必须为列表")
        try:
            filenameList = ast.literal_eval(filename)
            if isinstance(filenameList, list):  # 检查解析后的结果是否是列表
                pass
            else:
                raise ValueError("文件名必须为列表")
        except:
            raise ValueError("文件名必须为列表")
        if len(image)!= len(filenameList) :
            raise ValueError("生成图片数量与给定的文件名数量不对应")
        data = get_aliyun_ak(sts_service_url)
        access_key_id = data["data"]["accessKeyId"]
        access_key_secret = data["data"]["accessKeySecret"]
        security_token = data["data"]["securityToken"]

        n = 0
        for i in image:
            img = tensor_to_pil(i)
            put_object(img,filenameList[n],access_key_id, access_key_secret, security_token,bucket_name, endpoint)
            n = n + 1

        return ()


class LoadImageFromURL(Ac):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url": ("STRING",{"default":"https://gd-hbimg.huaban.com/5c6487e9ef2d4e4840082b0671cf3a86f8139eb430c1b-dLDkjJ_fw658webp"}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"
    def load_image(self, image_url):
        return read_image_from_url(image_url)
 
class LoadImageFromOss(Ac):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename": ("STRING",{"default":"tmp/screenshot.png"}),
                "access_key_id": ("STRING", {"default": "access_key_id"}),
                "access_key_secret": ("STRING", {"default": "access_key_secret"}),
                "security_token": ("STRING", {"default": ""}),
                "bucket_name": ("STRING", {"default": "bucket_name"}),
                "endpoint": (OSS_ENDPOINT_LIST,{"default": "oss-cn-shenzhen.aliyuncs.com"}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"
    def load_image(self, filename, access_key_id, access_key_secret, security_token, bucket_name, endpoint):
        return get_object(filename, access_key_id, access_key_secret, security_token, bucket_name, endpoint)
    
class LoadImageFromOssBySTSServiceUrl(Ac):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename": ("STRING",{"default":"comfyui/filename.png"}),
                "sts_service_url": ("STRING", {"default": "https://demo.cn/sts_service"}),
                "bucket_name": ("STRING", {"default": "bucket_name"}),
                "endpoint": (OSS_ENDPOINT_LIST,{"default": "oss-cn-shenzhen.aliyuncs.com"}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"
    def load_image(self, filename, sts_service_url,  bucket_name, endpoint):
        data = get_aliyun_ak(sts_service_url)
        access_key_id = data["data"]["accessKeyId"]
        access_key_secret = data["data"]["accessKeySecret"]
        security_token = data["data"]["securityToken"]
        return get_object(filename, access_key_id, access_key_secret, security_token, bucket_name, endpoint)