QT += core gui opengl openglwidgets

CONFIG += console qt c++11

DEFINES += QT_DEPRECATED_WARNINGS

INCLUDEPATH += "./glm"
INCLUDEPATH += "D:\Program\Code\Temp\HEAD\OpenGL\glew-2.1.0\include"

LIBS += \
	Glu32.lib \
	OpenGL32.lib
LIBS += glew32.lib

SOURCES += \
    main.cpp \
    myglwidget.cpp \
    utils.cpp

HEADERS += \
    myglwidget.h  \
    utils.h