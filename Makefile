ci:
	git add -u && git commit -m "Update" && git push

CXXFLAGS = -Wall \
					 -Wextra \
					 -Wnon-virtual-dtor \
					 -Wold-style-cast \
					 -Wcast-align \
					 -Wconversion \
					 -Wdouble-promotion \
					 -Wno-nested-anon-types \
					 -Wsign-conversion \
					 -Wformat=2 \
					 -Wimplicit-fallthrough \
					 -pedantic \
					 -fno-exceptions \
					 -fno-rtti \
					 -stdlib=libc++ \
					 -std=c++20 \
					 -fno-omit-frame-pointer \
					 -g3 -O3

BEAR := $(shell command -v bear 2> /dev/null)
SRC = $(shell ls -1 *.cpp)
OBJ = $(SRC:%.cpp=%.o)
DEP = $(SRC:%.cpp=%.d)

.PHONY: build
build:
ifndef BEAR
	@$(MAKE) build0
else
	@$(BEAR) --append -- $(MAKE) build0
endif

.PHONY: build0
build0: main

main: $(OBJ)
	@echo "ld $@"
	@$(CXX) $(LDFLAGS) $(CXXFLAGS) $(OBJ) -o $@

%.o: %.cpp Makefile
	@echo "cc $@"
	@$(CXX) $(CXXFLAGS) -o $@ -c $< -MD -MP
