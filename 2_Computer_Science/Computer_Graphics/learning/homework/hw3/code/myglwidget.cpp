#include "myglwidget.h"
#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
#include <algorithm>


MyGLWidget::MyGLWidget(QWidget *parent)
    : QOpenGLWidget(parent)
{
}

MyGLWidget::~MyGLWidget()
{
    makeCurrent();
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    glDeleteProgram(shaderProgram);
    doneCurrent();
}

void MyGLWidget::keyPressEvent(QKeyEvent* e)
{
    switch (e->key()) {
        case Qt::Key_1: rotationX += 0.1f; update(); break;
        case Qt::Key_2: rotationY += 0.1f; update(); break;
        case Qt::Key_3: rotationZ += 0.1f; update(); break;
    }
}

void MyGLWidget::resizeGL(int w, int h)
{
    WindowSizeW = w;
    WindowSizeH = h;
    glViewport(0, 0, w, h);
    projMatrix = glm::perspective(glm::radians(35.0f), (float)w / h, 0.1f, 2000.0f);
}

void MyGLWidget::initializeGL()
{
    initializeOpenGLFunctions();
    
    WindowSizeW = width();
    WindowSizeH = height();

    glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
    glEnable(GL_DEPTH_TEST);

    initScene();
    initShaders();
    initBuffers();
}

void MyGLWidget::initScene()
{
    objModel.loadModel("./objs/teapot_8000.obj");

    vec3 center = objModel.centralPoint;
    mat4 centerTransform = glm::translate(mat4(1.0f), -center);
    for (auto& vertex : objModel.vertices_data) {
        vec4 centered = centerTransform * vec4(vertex, 1.0f);
        vertex = vec3(centered);
    }
    objModel.centralPoint = vec3(0.0f);

    camPosition = vec3(100, 100, 100);
    camLookAt = vec3(0.0f);
    camUp = vec3(0, 1, 0);
    projMatrix = glm::perspective(glm::radians(35.0f), (float)WindowSizeW / (float)WindowSizeH, 0.1f, 2000.0f);
    lightPosition = vec3(0, 100, 100);
}

void MyGLWidget::initShaders()
{
    // Read vertex shader
    std::ifstream vertexFile("shaders/vertex_shader.glsl");
    std::string vertexSource((std::istreambuf_iterator<char>(vertexFile)),
                              std::istreambuf_iterator<char>());
    const char* vertexShaderSource = vertexSource.c_str();

    // Read fragment shader
    std::ifstream fragmentFile("shaders/fragment_shader.glsl");
    std::string fragmentSource((std::istreambuf_iterator<char>(fragmentFile)),
                                std::istreambuf_iterator<char>());
    const char* fragmentShaderSource = fragmentSource.c_str();

    // Compile vertex shader
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    // Compile fragment shader
    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    // Link shaders
    shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    // Delete shaders as they're linked into our program now and no longer necessary
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
}

void MyGLWidget::initBuffers()
{
    std::vector<float> vertexData;
    std::vector<uint> indices;
    vertexData.reserve(objModel.triangleCount * 18); // 3 vertices * (3 pos + 3 normal) floats
    indices.reserve(objModel.triangleCount * 3);
    for (uint i = 0; i < static_cast<unsigned int>(objModel.triangleCount); ++i) {
        for (uint j = 0; j < 3; ++j) {
            const auto& vertex = objModel.vertices_data[objModel.triangles[i][j]];
            const auto& normal = objModel.normals_data[objModel.triangle_normals[i][j]];
            vertexData.insert(vertexData.end(), {vertex.x, vertex.y, vertex.z, normal.x, normal.y, normal.z});
        }
        indices.insert(indices.end(), {i*3, i*3+1, i*3+2});
    }

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(float), vertexData.data(), GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size() * sizeof(unsigned int), indices.data(), GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindVertexArray(0);
}

void MyGLWidget::paintGL()
{
    auto start_time = std::chrono::high_resolution_clock::now();

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glUseProgram(shaderProgram);

    mat4 model = mat4(1.0f);
    model = glm::rotate(model, rotationX, vec3(1.0f, 0.0f, 0.0f));
    model = glm::rotate(model, rotationY, vec3(0.0f, 1.0f, 0.0f));
    model = glm::rotate(model, rotationZ, vec3(0.0f, 0.0f, 1.0f));
    mat4 view = glm::lookAt(camPosition, camLookAt, camUp);

    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, glm::value_ptr(model));
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "view"), 1, GL_FALSE, glm::value_ptr(view));
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "projection"), 1, GL_FALSE, glm::value_ptr(projMatrix));

    glUniform3fv(glGetUniformLocation(shaderProgram, "lightPos"), 1, glm::value_ptr(lightPosition));
    glUniform3fv(glGetUniformLocation(shaderProgram, "viewPos"), 1, glm::value_ptr(camPosition));
    glUniform3fv(glGetUniformLocation(shaderProgram, "lightColor"), 1, glm::value_ptr(lightColor));
    glUniform3fv(glGetUniformLocation(shaderProgram, "objectColor"), 1, glm::value_ptr(objectColor));

    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, objModel.triangleCount * 3, GL_UNSIGNED_INT, 0);
    glBindVertexArray(0);

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    qDebug() << "Render time:" << duration.count() << "microseconds";
}