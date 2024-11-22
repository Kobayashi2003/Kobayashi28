#include "myglwidget.h"

MyGLWidget::MyGLWidget(QWidget *parent)
    : QOpenGLWidget(parent),
      scene_id(0)
{
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(updateRotation()));
    timer->start(16); 
}

MyGLWidget::~MyGLWidget()
{
}

void MyGLWidget::initializeGL()
{
    glViewport(0, 0, width(), height());
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    glDisable(GL_DEPTH_TEST);
}

void MyGLWidget::paintGL()
{
    switch (scene_id)
    {
        case 0: scene_0(); break;
        case 1: scene_1(); break;
        case 2: scene_2(); break;
        case 3: scene_3(); break;
        case 4: scene_4(); break;
        case 5: scene_5(); break;
        case 6: scene_6(); break;
        case 7: scene_7(); break;
        case 10: scene_a(); break;
        case 11: scene_b(); break;
        case 12: scene_c(); break;
        case 13: scene_d(); break;
        default: scene_0(); break;
    }
}

void MyGLWidget::resizeGL(int width, int height)
{
    glViewport(0, 0, width, height);
    update();
}

void MyGLWidget::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_0) {
        scene_id = 0;
        update();
    }
    else if (e->key() == Qt::Key_1) {
        scene_id = 1;
        update();
    }
    else if (e->key() == Qt::Key_2) {
        scene_id = 2;
        update();
    }
    else if (e->key() == Qt::Key_3) {
        scene_id = 3;
        update();
    }
    else if (e->key() == Qt::Key_4) {
        scene_id = 4;
        update();
    }
    else if (e->key() == Qt::Key_5) {
        scene_id = 5;
        update();
    }
    else if (e->key() == Qt::Key_6) {
        scene_id = 6;
        update();
    }
    else if (e->key() == Qt::Key_7) {
        scene_id = 7;
        update();
    }
    else if (e->key() == Qt::Key_A) {
        scene_id = 10;
        update();
    }
    else if (e->key() == Qt::Key_B) {
        scene_id = 11;
        update();
    }
    else if (e->key() == Qt::Key_C) {
        scene_id = 12;
        update();
    }
    else if (e->key() == Qt::Key_D) {
        scene_id = 13;
        update();
    }
}

void MyGLWidget::updateRotation()
{
    rotationX += 0.5f;
    rotationY += 0.7f;
    rotationZ += 0.3f;

    if (rotationX > 360.0f)
        rotationX -= 360.0f;
    if (rotationY > 360.0f)
        rotationY -= 360.0f;
    if (rotationZ > 360.0f)
        rotationZ -= 360.0f;

    update(); // Request a repaint
}

void draw_L_line()
{
    glBegin(GL_LINE_LOOP);
    glVertex2f(-120.0f, 80.0f);
    glVertex2f(-100.0f, 80.0f);
    glVertex2f(-100.0f, -40.0f);
    glVertex2f(-60.0f, -40.0f);
    glVertex2f(-60.0f, -60.0f);
    glVertex2f(-120.0f, -60.0f);
    glVertex2f(-120.0f, -60.0f);
    glEnd();
}

void draw_L_1()
{
    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-120.0f, 80.0f);
    glVertex2f(-100.0f, 80.0f);
    glVertex2f(-120.0f, -60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(-100.0f, 80.0f);
    glVertex2f(-120.0f, -60.0f);
    glVertex2f(-100.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-120.0f, -60.0f);
    glVertex2f(-100.0f, -40.0f);
    glVertex2f(-60.0f, -60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(-100.0f, -40.0f);
    glVertex2f(-60.0f, -60.0f);
    glVertex2f(-60.0f, -40.0f);
    glEnd();
}

void draw_L_2()
{
    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-120.0f, 80.0f);
    glVertex2f(-100.0f, 80.0f);
    glVertex2f(-120.0f, -60.0f);
    glVertex2f(-100.0f, -40.0f);
    glVertex2f(-60.0f, -60.0f);
    glVertex2f(-60.0f, -40.0f);
    glEnd();
}

void draw_L_3()
{
    glBegin(GL_QUAD_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-120.0f, 80.0f);
    glVertex2f(-100.0f, 80.0f);
    glVertex2f(-120.0f, -60.0f);
    glVertex2f(-100.0f, -40.0f);
    glVertex2f(-60.0f, -60.0f);
    glVertex2f(-60.0f, -40.0f);
    glEnd();
}

void draw_J_line()
{
    glBegin(GL_LINE_LOOP);
    glVertex2f(10.0f, 80.0f);
    glVertex2f(30.0f, 80.0f);
    glVertex2f(30.0f, -40.0f);
    glVertex2f(10.0f, -60.0f);
    glVertex2f(-30.0f, -60.0f);
    glVertex2f(-30.0f, -40.0f);
    glVertex2f(10.0f, -40.0f);
    glEnd();
}

void draw_J_1()
{
    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(30.0f, 80.0f);
    glVertex2f(10.0f, 80.0f);
    glVertex2f(30.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(10.0f, 80.0f);
    glVertex2f(30.0f, -40.0f);
    glVertex2f(10.0f, -60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-30.0f, -60.0f);
    glVertex2f(10.0f, -60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-30.0f, -40.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-30.0f, -60.0f);
    glEnd();
}

void draw_J_2()
{
    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(30.0f, 80.0f);
    glVertex2f(10.0f, 80.0f);
    glVertex2f(30.0f, -40.0f);
    glVertex2f(10.0f, -60.0f);
    glEnd();

    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(10.0f, -60.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-30.0f, -60.0f);
    glVertex2f(-30.0f, -40.0f);
    glEnd();
}

void draw_J_3()
{
    glBegin(GL_QUAD_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(30.0f, 80.0f);
    glVertex2f(10.0f, 80.0f);
    glVertex2f(30.0f, -40.0f);
    glVertex2f(10.0f, -60.0f);
    glEnd();

    glBegin(GL_QUAD_STRIP);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(10.0f, -60.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-30.0f, -60.0f);
    glVertex2f(-30.0f, -40.0f);
    glEnd();
}

void draw_Z_line()
{
    glBegin(GL_LINE_LOOP);
    glVertex2f(60.0f, 80.0f);
    glVertex2f(120.0f, 80.0f);
    glVertex2f(120.0f, 60.0f);
    glVertex2f(80.0f, -40.0f);
    glVertex2f(120.0f, -40.0f);
    glVertex2f(120.0f, -60.0f);
    glVertex2f(60.0f, -60.0f);
    glVertex2f(60.0f, -40.0f);
    glVertex2f(100.0f, 60.0f);
    glVertex2f(60.0f, 60.0f);
    glEnd();
}

void draw_Z_1()
{
    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(60.0f, 80.0f);
    glVertex2f(120.0f, 80.0f);
    glVertex2f(60.0f, 60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(120.0f, 80.0f);
    glVertex2f(60.0f, 60.0f);
    glVertex2f(120.0f, 60.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(120.0f, 60.0f);
    glVertex2f(100.0f, 60.0f);
    glVertex2f(80.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(100.0f, 60.0f);
    glVertex2f(80.0f, -40.0f);
    glVertex2f(60.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(60.0f, -40.0f);
    glVertex2f(60.0f, -60.0f);
    glVertex2f(120.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(60.0f, -60.0f);
    glVertex2f(120.0f, -40.0f);
    glVertex2f(120.0f, -60.0f);
    glEnd();
}

void draw_Z_2()
{
    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(60.0f, 80.0f);
    glVertex2f(120.0f, 80.0f);
    glVertex2f(60.0f, 60.0f);
    glVertex2f(120.0f, 60.0f);
    glEnd();

    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(120.0f, 60.0f);
    glVertex2f(100.0f, 60.0f);
    glVertex2f(80.0f, -40.0f);
    glVertex2f(60.0f, -40.0f);
    glEnd();

    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex2f(60.0f, -40.0f);
    glVertex2f(60.0f, -60.0f);
    glVertex2f(120.0f, -40.0f);
    glVertex2f(120.0f, -60.0f);
    glEnd();
}

void draw_Z_3()
{
    glBegin(GL_QUAD_STRIP);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(60.0f, 80.0f);
    glVertex2f(120.0f, 80.0f);
    glVertex2f(60.0f, 60.0f);
    glVertex2f(120.0f, 60.0f);
    glEnd();

    glBegin(GL_QUAD_STRIP);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(120.0f, 60.0f);
    glVertex2f(100.0f, 60.0f);
    glVertex2f(80.0f, -40.0f);
    glVertex2f(60.0f, -40.0f);
    glEnd();

    glBegin(GL_QUAD_STRIP);
    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex2f(60.0f, -40.0f);
    glVertex2f(60.0f, -60.0f);
    glVertex2f(120.0f, -40.0f);
    glVertex2f(120.0f, -60.0f);
    glEnd();
}

void draw_L_3d()
{
    // Front face - Red
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUAD_STRIP);
    glVertex3f(-10.0f, 80.0f, 10.0f);
    glVertex3f(10.0f, 80.0f, 10.0f);
    glVertex3f(-10.0f, -60.0f, 10.0f);
    glVertex3f(10.0f, -40.0f, 10.0f);
    glVertex3f(50.0f, -60.0f, 10.0f);
    glVertex3f(50.0f, -40.0f, 10.0f);
    glEnd();

    // Back face - Green
    glColor3f(0.0f, 1.0f, 0.0f);
    glBegin(GL_QUAD_STRIP);
    glVertex3f(-10.0f, 80.0f, -10.0f);
    glVertex3f(10.0f, 80.0f, -10.0f);
    glVertex3f(-10.0f, -60.0f, -10.0f);
    glVertex3f(10.0f, -40.0f, -10.0f);
    glVertex3f(50.0f, -60.0f, -10.0f);
    glVertex3f(50.0f, -40.0f, -10.0f);
    glEnd();

    // Side faces - Blue
    glColor3f(0.0f, 0.0f, 1.0f);
    glBegin(GL_QUAD_STRIP);
    glVertex3f(-10.0f, 80.0f, 10.0f);
    glVertex3f(-10.0f, 80.0f, -10.0f);
    glVertex3f(10.0f, 80.0f, 10.0f);
    glVertex3f(10.0f, 80.0f, -10.0f);
    glVertex3f(10.0f, -40.0f, 10.0f);
    glVertex3f(10.0f, -40.0f, -10.0f);
    glVertex3f(50.0f, -40.0f, 10.0f);
    glVertex3f(50.0f, -40.0f, -10.0f);
    glVertex3f(50.0f, -60.0f, 10.0f);
    glVertex3f(50.0f, -60.0f, -10.0f);
    glVertex3f(-10.0f, -60.0f, 10.0f);
    glVertex3f(-10.0f, -60.0f, -10.0f);
    glVertex3f(-10.0f, 80.0f, 10.0f);
    glVertex3f(-10.0f, 80.0f, -10.0f);
    glEnd();
}

void MyGLWidget::setCommonProjection() {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0f, width(), 0.0f, height(), -1000.0f, 1000.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.5 * width(), 0.5 * height(), 0.0f);
}

void MyGLWidget::setOrthogonalProjection(int viewType)
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-width()/2, width()/2, -height()/2, height()/2, -1000.0f, 1000.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    if (viewType == 1) {
        // From (0, 0, d) looking at (0, 0, 0)
        gluLookAt(0.0, 0.0, d, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    } else {
        // From (0, 0.5*d, d) looking at (0, 0, 0)
        gluLookAt(0.0, 0.5*d, d, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    }

    glMatrixMode(GL_MODELVIEW);
    glTranslatef(0.0f, 0.0f, -d);
}

void MyGLWidget::setPerspectiveProjection(int viewType)
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (float)width() / (float)height(), 0.1, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    if (viewType == 1) {
        // From (0, 0, d) looking at (0, 0, 0)
        gluLookAt(0.0, 0.0, d, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    } else {
        // From (0, 0.5*d, d) looking at (0, 0, 0)
        gluLookAt(0.0, 0.5*d, d, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    }

    glMatrixMode(GL_MODELVIEW);
    glTranslatef(0.0f, 0.0f, -d);
}

void MyGLWidget::scene_0()
{
    glMatrixMode(GL_MODELVIEW);
    glTranslatef(0.0f, 0.0f, -d);
    setCommonProjection();

    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);

    draw_L_line();
    draw_J_line();
    draw_Z_line();
}

void MyGLWidget::scene_1()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);
    setCommonProjection();

    draw_L_1();
    draw_J_1();
    draw_Z_1();
}

void MyGLWidget::scene_2()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);
    setCommonProjection();

    draw_L_2();
    draw_J_2();
    draw_Z_2();
}

void MyGLWidget::scene_3()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);
    setCommonProjection();

    draw_L_3();
    draw_J_3();
    draw_Z_3();
}

void MyGLWidget::scene_4()
{
    setOrthogonalProjection(1);

    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);

    draw_L_line();
    draw_J_line();
    draw_Z_line();
}

void MyGLWidget::scene_5()
{
    setOrthogonalProjection(2);

    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);

    draw_L_line();
    draw_J_line();
    draw_Z_line();
}

void MyGLWidget::scene_6()
{
    setPerspectiveProjection(1);

    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);

    draw_L_line();
    draw_J_line();
    draw_Z_line();
}

void MyGLWidget::scene_7()
{
    setPerspectiveProjection(2);

    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0f, 0.0f, 0.0f);

    draw_L_line();
    draw_J_line();
    draw_Z_line();
}

void MyGLWidget::scene_a()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (GLfloat)width() / (GLfloat)height(), 0.1, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -200.0f); // Changed to center the L shape

    // Apply rotation
    glRotatef(rotationX, 1.0f, 0.0f, 0.0f);
    // glRotatef(rotationY, 0.0f, 1.0f, 0.0f);
    // glRotatef(rotationZ, 0.0f, 0.0f, 1.0f);

    draw_L_3d();

    glDisable(GL_DEPTH_TEST);
}

void MyGLWidget::scene_b()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (GLfloat)width() / (GLfloat)height(), 0.1, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -200.0f); // Changed to center the L shape

    // Apply rotation
    // glRotatef(rotationX, 1.0f, 0.0f, 0.0f);
    glRotatef(rotationY, 0.0f, 1.0f, 0.0f);
    // glRotatef(rotationZ, 0.0f, 0.0f, 1.0f);

    draw_L_3d();

    glDisable(GL_DEPTH_TEST);
}

void MyGLWidget::scene_c()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (GLfloat)width() / (GLfloat)height(), 0.1, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -200.0f); // Changed to center the L shape

    // Apply rotation
    // glRotatef(rotationX, 1.0f, 0.0f, 0.0f);
    // glRotatef(rotationY, 0.0f, 1.0f, 0.0f);
    glRotatef(rotationZ, 0.0f, 0.0f, 1.0f);

    draw_L_3d();

    glDisable(GL_DEPTH_TEST);
}

void MyGLWidget::scene_d()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (GLfloat)width() / (GLfloat)height(), 0.1, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -200.0f); // Changed to center the L shape

    // Apply rotation
    glRotatef(rotationX, 1.0f, 0.0f, 0.0f);
    glRotatef(rotationY, 0.0f, 1.0f, 0.0f);
    glRotatef(rotationZ, 0.0f, 0.0f, 1.0f);

    draw_L_3d();

    glDisable(GL_DEPTH_TEST);
}