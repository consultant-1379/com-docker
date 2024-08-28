#
# CMake toolchain file for RCS x86_64
#
# Items marked with XXX require an action in order to use this toolchain
# file to build COM outside COM development environment.
#
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_VERSION 1)
set(TARGET_ARCHITECTURE "x86_64")

# Sysroot
# XXX If you are not a COM Developer, you will have to modify this with
#     the path where you store your sysroot
set(SYSROOT $ENV{SYSROOT})
set(SYSROOT_LD_LIBRARY_PATH "${SYSROOT}/lib64:${SYSROOT}/usr/lib64")

# Set compiler options, the "CACHE STRING FORCE" is a workaround to make sure
# flags are used in CMake compiler tests.
# XXX Here you can add your own compiler and linker flags. If you tell COM about
#     the flags you want, they can probably add them to this file, so COM deliveries
#     are tested with your flags.
#
set(CMAKE_C_FLAGS "-m64 --sysroot=${SYSROOT} -Wno-unused-local-typedefs" CACHE STRING "" FORCE)    # C Compiler flags
set(CMAKE_CXX_FLAGS "-m64 --sysroot=${SYSROOT} -Wno-unused-local-typedefs" CACHE STRING "" FORCE)  # C++ Compiler flags
set(CMAKE_EXE_LINKER_FLAGS "-m64 -Wl,--dynamic-linker=${SYSROOT}/lib64/ld-linux-x86-64.so.2" CACHE STRING "" FORCE) # Linker flags


# We need to make sure LD_RUN_PATH does not affect the RPATH of the binary, so
# we set it ourselves. RCS will use LD_LIBRARY_PATH when running COM to point
# to their sysroot.
#
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "${SYSROOT_LD_LIBRARY_PATH}")

# Prefix search locations
set(CMAKE_FIND_ROOT_PATH
    ${SYSROOT}
)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
