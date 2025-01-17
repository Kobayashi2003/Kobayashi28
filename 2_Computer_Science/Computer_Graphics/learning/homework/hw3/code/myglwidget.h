#ifndef MYGLWIDGET_H
#define MYGLWIDGET_H

#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <QtGui>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLExtraFunctions>

#include "utils.h"

using namespace glm;

class MyGLWidget : public QOpenGLWidget, protected QOpenGLExtraFunctions {
    Q_OBJECT

public:
    MyGLWidget(QWidget *parent = nullptr);
    ~MyGLWidget();

protected:
    void initializeGL() override;
    void paintGL() override;
    void resizeGL(int width, int height) override;
    void keyPressEvent(QKeyEvent* e) override;

private:
    void initShaders();
    void initScene();
    void initBuffers();

    int WindowSizeH = 0;
    int WindowSizeW = 0;
    float rotationX = 0.0f;
    float rotationY = 0.0f;
    float rotationZ = 0.0f;

    Model objModel;

    vec3 camPosition;
    vec3 camLookAt;
    vec3 camUp;
    mat4 projMatrix;
    vec3 lightPosition;

    vec3 lightColor = vec3(1.0f, 1.0f, 1.0f);
    vec3 objectColor = vec3(1.0f, 0.5f, 0.31f);
    // vec3 objectColor = vec3(0.95f, 0.93f, 0.88f);

    GLuint shaderProgram;
    GLuint VAO, VBO, EBO;

    // 添加用于分批渲染的参数
    size_t totalTriangles = 0;        // 总三角形数量
    size_t verticesPerBatch = 0;      // 每批次的顶点数量
    size_t currentBatchOffset = 0;     // 当前批次的偏移量
    std::vector<float> vertexData;     // 用于存储当前批次的顶点数据
};

#endif // MYGLWIDGET_H