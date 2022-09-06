from block_scope import new_scope

a = 4
b = 5
with new_scope() as this:
    this.c = 10
    print("this.a", this.a)
    print("this.b", this.b)
    print("this.c", this.c)
print("this", this)
