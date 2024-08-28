# This file is an adaptation layer for the CodeChecker-based framework.
# It is sourced to the bash scripts of the framework and provides an API.
# When you plan to adapt your project to the framework, these functions
# should be ported.
# The framework binaries and this file should be placed in the same directory.
# The project specific helper scripts can be installed in other places.

# Query the file name of the "JSON compilation database".
# See http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Parameters:
# 1 - Directory where the database should be created.
#
# Return:
# Full name of the compilation database file.
#
get_compilation_database() {
    local target_dir=${1}
    local compile_commands_json="${target_dir}/compile_commands.json"

    echo "${compile_commands_json}"
}

# Query the logging controller flag. Returns true (0) if the project requires
# logging phase (pre-build) to produce "JSON compilation database".
#
# Return:
# 0 if the project needs lgging phase before parsing phase to produce compilation
# database on demand.
# 1 - When there is  compilation database that reachable by the framework at the
# moment of the parsing phase.
#
# Sometimes the logging phase is not necessary, for example the project has got
# a compilation database.
#
# COM:
#  Logging is necessary.
#
is_logging_necessary() {
    return 0
}



# Queries file name pattern of the observed compiler(s).
#
# Return:
# Colon separated program names as described in the CodeCompass documentation.
#
get_compiler_pattern() {
    echo "cc:c++:gcc:g++"
}


# Filter the file name of the "JSON compilation database".
# See http://clang.llvm.org/docs/JSONCompilationDatabase.html
# Generates a new filtered compilation database file.
# Parameters:
# 1 - Directory where the binaries of the frameworkwas installed.
# 2 - Directory where the database should be created.
#
# Return:
# Full name of the pre-processed/filtered compilation database file.
#
# Sometimes the compilation database contains unnecessary compile commands or
# requires modifications that allows the clang compiler to run well.
# This hook allows project specific editing before parsing phase.
#
filter_compilation_database() {
    local scriptdir="${1}"
    local compilation_database=$(readlink -e "${2}")
    local dir_name=$(dirname "${compilation_database}")
    local filtered_name="${dir_name}/filtered.$(basename ${compilation_database})"

    "${scriptdir}/filterbuildcmds.py" --input "${compilation_database}" \
        --output "${filtered_name}"
    echo "${filtered_name}"
}

# Queries additional CodeChecker analyze flags.
#
# Parameters:
# 1 - Directory where the binaries of the framework was installed.
#
# Return:
# Newline separated string of directory names.
#
get_analyze_flags_array() {
    local scriptdir="${1}" # Not used

    source "${CONFIG_DIR}/checker_flags"
    for flag in "${checker_flags[@]}"
    do
        echo "${flag}"
    done
}

# Generate a run-tag option for this analysis.
# It can be for example a hash of a particular commit in a git repository.
# It should be a complete "--tag <tag>" option pair or empty.
#
# Parameters:
# 1 - Directory where the project specific files can be stored.
#
# Return:
# A string that can be used as a tag for "CodeChecker store" command.
# Must not return an empty string.
#
generate_run_tag() {
    local workspacedir="${1}"
    local com_directory="${2}" #"${workspacedir}"
    local git_hash="$(git --git-dir="${com_directory}/.git" rev-parse HEAD)"

    echo "--tag ${git_hash}"
}



# Specify skip file options for the analysis phase of Code Checker.
#
# Return:
# A string that can be used as a tag for "CodeChecker store" command.
# It should be a complete "--ignore <SKIPFILE>" option pair or empty.
#
generate_skipfile_option() {
    local configdir="${1}"
    echo "--ignore ${configdir}/skipfile"
}
