cmake_minimum_required(VERSION 3.5)
project(Work)

set(CMAKE_CXX_STANDARD 17)

include_directories(.)
add_executable(Work main.cpp mywork.cpp Stable/IWork.cpp)
