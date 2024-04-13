#pragma once

#include <string>

class Game {

private:
    virtual void initDescription() = 0;
public:
    std::string gameName;
    std::string gameVersion;
    std::string gameAuthor;
public:
    Game() = default;
    virtual void showDescription() = 0; 
};