#
# Cmake toolchain file for RCS arm
#
# Items marked with XXX require an action in order to use this toolchain
# file to build COM outside COM development environment.
#
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_VERSION 1)
set(TARGET_ARCHITECTURE "arm")

# Sysroot
# XXX If you are not a COM Developer, you will have to modify this with
#     the path where you store your sysroot
set(SYSROOT $ENV{SYSROOT})

# Set compiler options, the "CACHE STRING FORCE" is a workaround to make sure
# flags are used in CMake compiler tests.
# XXX Here you can add your own compiler and linker flags. If you tell COM about
#     the flags you want, they can probably add them to this file, so COM deliveries
#     are tested with your flags.

set(CMAKE_C_FLAGS "--sysroot=${SYSROOT} -Wno-unused-local-typedefs" CACHE STRING "" FORCE)    # C Compiler flags
set(CMAKE_CXX_FLAGS "--sysroot=${SYSROOT} -Wno-unused-local-typedefs" CACHE STRING "" FORCE)  # C++ Compiler flags
set(CMAKE_EXE_LINKER_FLAGS "") # Linker flags

# Prefix search locations
set(CMAKE_FIND_ROOT_PATH
        ${SYSROOT}
)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

set(COM_INSTALL_PREFIX rcs/com CACHE STRING "COM install prefix")
set(FT_PSO_INSTALL_PREFIX rcs/com)
