# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++11 -Iinclude

# Source files
SRC_DIR = src
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Object files
OBJ_DIR = obj
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))

# Executable name
TARGET = bin/test

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Rule to build the executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Rule to build object files from source files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Create the object directory if it doesn't exist
#$(OBJ_DIR):
#	mkdir -p $(OBJ_DIR)

# Clean rule
clean:
	rm -rf $(OBJ_DIR) $(TARGET)

# Dependencies
$(OBJS): $(wildcard $(SRC_DIR)/*.h)