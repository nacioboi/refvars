# How to compile a DLL on Windows

## Compile with `cl` to object file

```cmd
cl /c /EHsc ..\compute.c
```

- The `/c` flag tells the compiler to compile the source file to an object file.
- The `/EHsc` flag tells the compiler to enable exception handling.

## Link the object file to a DLL

```cmd
link /DLL /OUT:compute.dll compute.obj
```

- The `/DLL` flag tells the linker to create a DLL.
- The `/OUT` flag specifies the output file name.
