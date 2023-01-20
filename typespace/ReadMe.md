Tasks:

1. TypeSpace is a group of type names as well as constraints for those types
2. TypeSpace is defined as a function annotated with @typespace decorator
3. TypeSpace function consist of list of type names (camel style) as function arguments
4. The body of type space function consist of assert statements that argument with such type must follow
5. To use types from typespace in certain function, this function should be decorated with typespaced function
6. Function arguments now can use types from typespace
7. Function arguments can use multiple types for single arguments. In this case this argument will participate in all assertments that are related to the types defined
8. Function can declare multiple arguments with same type. In this case each argument will participate in assertments where the type is used
9. If there are some assertments that use multiple types (for ex. assert Start<End) and there are few arguments with type Start and type End - all arguments will be compared in different combinations. So we will make sure all Start arguments are always less than End arguments
10. TODO