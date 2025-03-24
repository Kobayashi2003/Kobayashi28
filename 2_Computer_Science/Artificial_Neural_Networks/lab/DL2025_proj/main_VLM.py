## CLIP zero-shot
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
## install packages: torch, transformers==4.23.1


if __name__ == '__main__':
    print('Loading Model, wait for a minute.')
    # 加载 OpenAI 预训练好的 CLIP 模型，类型是ViT-B
    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name)
    model = model.eval()
    # 冻结模型参数，不进行训练
    for param in model.parameters():
        param.requires_grad = False
    # 加载 CLIP 模型（用于图像和文本的预处理）
    processor = CLIPProcessor.from_pretrained(model_name)

    image = Image.open(r"Photo path")
    # 预定义的文本标签（分类类别）
    text_labels = ["a photo of a cat", "a photo of a dog", "a photo of a horse"]
    # 预处理输入数据，将文本和图像转换为模型可接受的格式
    inputs = processor(text=text_labels, images=image, return_tensors="pt", padding=True)
    # 获取模型输出
    outputs = model(**inputs)
    # 获取图像与文本类别的相似度分数
    logits_per_image = outputs.logits_per_image
    # 计算 softmax 归一化后的概率
    probs = logits_per_image.softmax(dim=1)
    # 获取最高概率对应的索引
    predicted_label_idx = probs.argmax()

    # 打印预测结果
    print(predicted_label_idx)
    print(text_labels[predicted_label_idx])


