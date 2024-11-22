#ifndef MYGLWIDGET_H
#define MYGLWIDGET_H

#ifdef MAC_OS
#include <QtOpenGL/QtOpenGL>
#else
#include <GL/glew.h>
#endif
#include <QtGui>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QTimer>

class MyGLWidget : public QOpenGLWidget{
    Q_OBJECT

public:
    MyGLWidget(QWidget *parent = nullptr);
    ~MyGLWidget();

protected:
    void initializeGL();
    void paintGL();
    void resizeGL(int width, int height);
	void keyPressEvent(QKeyEvent *e);
    void setCommonProjection();
    void setOrthogonalProjection(int viewType);
    void setPerspectiveProjection(int viewType);

private:
	int scene_id;
	void scene_0();
	void scene_1();
    void scene_2();
    void scene_3();
    void scene_4();
    void scene_5();
    void scene_6();
    void scene_7();
    void scene_a();
    void scene_b();
    void scene_c();
    void scene_d();

    float d = 200.0f;
    float rotationX, rotationY, rotationZ;
    QTimer *timer;

private slots:
    void updateRotation();
};
#endif // MYGLWIDGET_H
