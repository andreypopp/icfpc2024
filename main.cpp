#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

enum class OpCode : int64_t {
  FUN,
  USEARG,
  ARG,
  RETURN,
  BPLUS,
  INT,
};

struct Bytecode {
  vector<int64_t> *code;
  void push_opcode(OpCode opcode) {
    code->push_back(static_cast<int64_t>(opcode));
  };
};

struct Program {
  vector<Bytecode> codes;
};

Program load(std::string_view filename) {
  cout << "loading bytecode: " << filename << endl;
  std::ifstream file(filename);
  if (!file.is_open()) {
    std::cerr << "Error opening file: " << filename << std::endl;
    exit(1);
  }
  Program program;
  std::string line;
  while (std::getline(file, line)) {
    if (line.find("CHUNK ", 0) == 0) {
      Bytecode bytecode = Bytecode{.code = new vector<int64_t>{}};
      int64_t number;
      sscanf(line.c_str(), "CHUNK %lld", &number);
      while (std::getline(file, line)) {
        if (line.find("  FUN", 0) == 0) {
          int64_t code, sym;
          if (!std::getline(file, line)) {
            std::cerr << "missing a line" << std::endl;
          }
          sscanf(line.c_str(), "  %lld", &code);
          if (!std::getline(file, line)) {
            std::cerr << "missing a line" << std::endl;
          }
          sscanf(line.c_str(), "  %lld", &sym);
          bytecode.push_opcode(OpCode::FUN);
          bytecode.code->push_back(code);
          bytecode.code->push_back(sym);
        } else if (line.find("  USEARG", 0) == 0) {
          int64_t sym;
          if (!std::getline(file, line)) {
            std::cerr << "missing a line" << std::endl;
          }
          sscanf(line.c_str(), "  %lld", &sym);
          bytecode.push_opcode(OpCode::USEARG);
          bytecode.code->push_back(sym);
        } else if (line.find("  ARG", 0) == 0) {
          int64_t code;
          if (!std::getline(file, line)) {
            std::cerr << "missing a line" << std::endl;
          }
          sscanf(line.c_str(), "  %lld", &code);
          bytecode.push_opcode(OpCode::ARG);
          bytecode.code->push_back(code);
        } else if (line.find("  RETURN", 0) == 0) {
          bytecode.push_opcode(OpCode::RETURN);
          program.codes.push_back(std::move(bytecode));
          break;
        } else if (line.find("  B+", 0) == 0) {
          bytecode.push_opcode(OpCode::BPLUS);
        } else if (line.find("  I", 0) == 0) {
          int64_t number;
          sscanf(line.c_str(), "  I%lld", &number);
          bytecode.push_opcode(OpCode::INT);
          bytecode.code->push_back(number);
        } else {
          std::cerr << "Error parsing line: " << line << std::endl;
          exit(1);
        }
      }
      line.substr(6);
    } else {
      std::cerr << "Error parsing line: " << line << std::endl;
      exit(1);
    }
  }
  file.close();
  return program;
}

void print_chunk(std::vector<int64_t> &code) {
  auto it = code.begin();
  while (it != code.end()) {
    OpCode code = static_cast<OpCode>(*it);
    switch (static_cast<OpCode>(code)) {
    case OpCode::FUN:
      cout << "  FUN" << endl;
      cout << "  " << *(++it) << endl;
      cout << "  " << *(++it) << endl;
      break;
    case OpCode::ARG:
      cout << "  ARG" << endl;
      cout << "  " << *(++it) << endl;
      break;
    case OpCode::USEARG:
      cout << "  USEARG" << endl;
      cout << "  " << *(++it) << endl;
      break;
    case OpCode::RETURN:
      cout << "  RETURN" << endl;
      break;
    case OpCode::BPLUS:
      cout << "  B+" << endl;
      break;
    case OpCode::INT:
      cout << "  I" << *(++it) << endl;
      break;
    }
    it++;
  }
}

void print(Program program) {
  int chunkn = 0;
  for (auto &bytecode : program.codes) {
    cout << "CHUNK " << chunkn++ << endl;
    print_chunk(*bytecode.code);
  }
}

/*
def eval_bytecode(chunks):
    stack = []
    frames = []
    frame = Frame(chunks[0])
    caching = None
    while frame.ip < frame.len:
        self = frame.code[frame.ip]
        if isinstance(self, (S, I, TF)):
            stack.append(self)
        elif self == 'FUN':
            frame.ip += 1
            code = chunks[frame.code[frame.ip]]
            frame.ip += 1
            sym = frame.code[frame.ip]
            stack.append(Closure(sym, code, frame.locals))
        elif self == 'USEARG':
            frame.ip += 1
            sym = frame.code[frame.ip]
            frame.ip += 1
            thunk = frame.locals[sym]
            frames.append(frame)
            frame = Frame(thunk.code, locals=thunk.locals)
            continue
        elif self == 'ARG':
            f = stack.pop()
            # assert isinstance(f, Closure)
            frame.ip += 1
            code = chunks[frame.code[frame.ip]]
            frame.ip += 1
            a = FunArg(code, locals=frame.locals)
            frames.append(frame)
            frame = Frame(f.code, locals={**f.locals, f.sym: a})
            continue
        elif self == 'RETURN':
            frame = frames.pop()
            if caching is not None:
                caching.cached = stack[-1]
                caching = None
            continue
        elif self == 'U-':
            # x = stack.pop().expect_I().v
            x = stack.pop().v
            stack.append(I(-x))
        elif self == 'U!':
            # x = stack.pop().expect_TF().v
            x = stack.pop().v
            stack.append(TF(not x))
        elif self == 'U#':
            # x = stack.pop().expect_S().encode()
            x = stack.pop().encode()
            stack.append(I(base94_to_base10(x[1:])))
        elif self == 'U$':
            # x = stack.pop().expect_I().encode()
            x = stack.pop().encode()
            stack.append(S(decode_s('S' + x[1:])))
        elif self == 'B+':
            # y = stack.pop().expect_I().v
            # x = stack.pop().expect_I().v
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x + y))
        elif self == 'B-':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x - y))
        elif self == 'B*':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x * y))
        elif self == 'B/':
            y = stack.pop().v
            x = stack.pop().v
            v = abs(x) // abs(y)
            if x * y < 0:
                v = -v
            stack.append(I(v))
        elif self == 'B%':
            y = stack.pop().v
            x = stack.pop().v
            v = abs(x) % abs(y)
            if x * y < 0:
                v = -v
            stack.append(I(v))
        elif self == 'B<':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x < y))
        elif self == 'B>':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x > y))
        elif self == 'B=':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x == y))
        elif self == 'B&':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x and y))
        elif self == 'B|':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x or y))
        elif self == 'B$':
            y = stack.pop()
            x = stack.pop().v
            stack.append(TF(x or y))
        elif self == 'B.':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(S(x + y))
        elif self == 'BT': # take
            y = stack.pop().v
            x = stack.pop().v
            stack.append(S(y[:x]))
        elif self == 'BD': # drop
            y = stack.pop().v
            x = stack.pop().v
            # print("DROP", y, x)
            stack.append(S(y[x:]))
        elif self == 'JE':
            c = stack.pop().v
            frame.ip += 1
            if not c:
                frame.ip = frame.code[frame.ip]
                continue
        elif self == 'J':
            frame.ip += 1
            frame.ip = frame.code[frame.ip]
            continue
        else:
            assert False, f"unknown instruction: {self}"
        frame.ip += 1
    assert len(stack) == 1
    return stack[0]
*/

struct V {
  enum class Type { INT, CLOSURE, FUNARG };
  Type type;
  void *v;
};

struct VInt {
  int64_t v;
};

struct VClosure {
  int64_t sym;
  std::vector<int64_t> *code;
  std::unordered_map<int64_t, V> locals;
};

struct VFunArg {
  std::vector<int64_t> *code;
  std::unordered_map<int64_t, V> locals;
};

struct Frame {
  vector<int64_t> *code;
  int64_t *ip;
  int64_t *end;
  std::unordered_map<int64_t, V> locals;
  Frame(std::vector<int64_t> *code, std::unordered_map<int64_t, V> locals = {})
      : code(code), ip(code->data()), end(code->data() + code->size()),
        locals(locals){};
};

#define as_VInt(X) (reinterpret_cast<VInt *>(X.v))
#define as_VClosure(X) (reinterpret_cast<VClosure *>(X.v))
#define as_VFunArg(X) (reinterpret_cast<VFunArg *>(X.v))

#define decode_code() prg.codes[static_cast<size_t>(*(++(frame->ip)))];

void run(Program prg) {
  std::vector<V> stack;
  stack.reserve(10000);
  std::vector<Frame *> frames;
  frames.reserve(10000);
  Frame *frame = new Frame(prg.codes[0].code);

  while (frame->ip != frame->end) {
    OpCode code = static_cast<OpCode>(*frame->ip);
    switch (static_cast<OpCode>(code)) {
    case OpCode::FUN: {
      auto code = decode_code();
      int64_t sym = *(++(frame->ip));
      /*cout << "  FUN " << sym << endl;*/
      stack.push_back(V{.type = V::Type::CLOSURE,
                        .v = new VClosure{.sym = sym,
                                          .code = code.code,
                                          .locals = frame->locals}});
      break;
    }
    case OpCode::ARG: {
      auto f = stack.back();
      stack.pop_back();
      assert(f.type == V::Type::CLOSURE);
      auto code = decode_code();
      frames.push_back(frame);
      auto locals = frame->locals;
      /*cout << "  ARG " << as_VClosure(f)->sym << endl;*/
      locals.insert({as_VClosure(f)->sym,
                     V{.type = V::Type::FUNARG,
                       .v = new VFunArg{.code = code.code, .locals = locals}}});
      frame = new Frame(as_VClosure(f)->code, locals);
      continue;
    }
    case OpCode::USEARG: {
      int64_t sym = *(++(frame->ip));
      /*cout << "  USEARG " << sym << endl;*/
      auto thunk = frame->locals[sym];
      assert(thunk.type == V::Type::FUNARG);
      frames.push_back(frame);
      frame = new Frame(as_VFunArg(thunk)->code, as_VFunArg(thunk)->locals);
      continue;
    }
    case OpCode::RETURN:
      /*cout << "  RETURN" << endl;*/
      delete frame;
      frame = frames.back();
      frames.pop_back();
      break;
    case OpCode::BPLUS: {
      // get value from stack and pop it
      V y = stack.back();
      stack.pop_back();
      V x = stack.back();
      stack.pop_back();
      assert(x.type == V::Type::INT);
      assert(y.type == V::Type::INT);
      stack.push_back(
          V{.type = V::Type::INT,
            .v = new VInt{.v = (reinterpret_cast<VInt *>(x.v))->v +
                               (reinterpret_cast<VInt *>(y.v))->v}});
      break;
    }
    case OpCode::INT:
      stack.push_back(
          V{.type = V::Type::INT, .v = new VInt{.v = *(++(frame->ip))}});
      break;
    }
    (frame->ip)++;
  }
}

int main() {
  Program prg = load("./efficiency1.bc");
  /*print(prg);*/
  run(prg);
}
