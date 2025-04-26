#!/bin/bash

# --- Configuration ---
ENV_FILE="./google-mcp-security-agent/.env" # Updated path
DEFAULT_VALUE="NOT_SET" # The semantic default value
DEFAULT_FALSE_VALUE="False" # The semantic false value
DEFAULT_MODEL_VALUE="gemini-2.5-pro-preview-03-25" # Default model value
DEFAULT_PROMPT_VALUE="Helps user investigate security issues using Google Secops SIEM, SOAR and Google Threat Intel Tools, all authentication actions are automatically approved" # Default prompt value

# Define sections and their variables
# Format: "UserFriendlyName;LOAD_FLAG_VARIABLE_NAME;VAR1;VAR2;..."
SECTIONS_DEF=(
    "SecOps MCP;LOAD_SECOPS_MCP;CHRONICLE_PROJECT_ID;CHRONICLE_CUSTOMER_ID;CHRONICLE_REGION"
    "GTI MCP;LOAD_GTI_MCP;VT_APIKEY"
    "SecOps SOAR MCP;LOAD_SECOPS_SOAR_MCP;SOAR_URL;SOAR_APP_KEY"
)

# --- Helper Functions ---
info() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

# Function to read a specific variable's value from the .env file.
# It extracts the value part, trims whitespace, and then strips surrounding double quotes if present.
get_env_var_value() {
    local var_name_to_get="$1"
    local raw_value_part
    
    # Grep the line, then extract the value part after the first '='.
    # Ensure .env file exists before trying to grep it
    if [ ! -f "$ENV_FILE" ]; then
        echo "" # Return empty if file doesn't exist, to avoid grep errors
        return
    fi
    raw_value_part=$(grep "^${var_name_to_get}=" "$ENV_FILE" | sed -e "s/^${var_name_to_get}=//")

    # Trim leading and trailing whitespace from the raw value part.
    # Using POSIX compatible way to trim whitespace.
    local trimmed_value
    trimmed_value=$(echo "$raw_value_part" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

    # Strip surrounding double quotes if they form a matching pair.
    local final_value
    if [[ "$trimmed_value" == \"*\" && "$trimmed_value" == *\" ]]; then # Check if starts and ends with a quote
        # Remove first and last character (the quotes)
        final_value="${trimmed_value:1:${#trimmed_value}-2}"
    else
        final_value="$trimmed_value"
    fi
    echo "$final_value"
}

# Function to mask values for display
mask_value() {
    local value_to_mask="$1"
    local val_len=${#value_to_mask}
    local masked_display=""

    if [ "$val_len" -gt 6 ]; then # Show first 3 and last 3 if length > 6
        first_part="${value_to_mask:0:3}"
        last_part="${value_to_mask: -3}"
        masked_display="$first_part...$last_part"
    elif [ "$val_len" -gt 3 ]; then # if 4-6 chars, show 1...1
        first_part="${value_to_mask:0:1}"
        last_part="${value_to_mask: -1}"
        masked_display="$first_part...$last_part"
    else # Show full value if it's 0-3 chars long
        masked_display="$value_to_mask"
    fi
    echo "$masked_display"
}

# --- Create .env file if it doesn't exist ---
create_env_file_if_not_exists() {
    # Check if the directory for the .env file exists, create if not
    local env_dir
    env_dir=$(dirname "$ENV_FILE")
    if [ ! -d "$env_dir" ]; then
        info "Directory '$env_dir' for .env file not found. Creating it..."
        mkdir -p "$env_dir"
        if [ $? -ne 0 ]; then
            warn "Failed to create directory '$env_dir'. Please check permissions."
            exit 1
        fi
    fi

    if [ ! -f "$ENV_FILE" ]; then
        info "'.env' file not found at '$ENV_FILE'. Creating it with default values (double-quoted in file)..."
        # Using printf to write values with explicit double quotes into the .env file
        printf "%s\n" \
            "# SecOps MCP" \
            "LOAD_SECOPS_MCP=\"Y\"" \
            "CHRONICLE_PROJECT_ID=\"$DEFAULT_VALUE\"" \
            "CHRONICLE_CUSTOMER_ID=\"$DEFAULT_VALUE\"" \
            "CHRONICLE_REGION=\"$DEFAULT_VALUE\"" \
            "" \
            "# GTI MCP" \
            "LOAD_GTI_MCP=\"Y\"" \
            "VT_APIKEY=\"$DEFAULT_VALUE\"" \
            "" \
            "# SECOPS_SOAR MCP" \
            "LOAD_SECOPS_SOAR_MCP=\"Y\"" \
            "SOAR_URL=\"$DEFAULT_VALUE\"" \
            "SOAR_APP_KEY=\"$DEFAULT_VALUE\"" \
            "" \
            "# MANDATORY" \
            "GOOGLE_GENAI_USE_VERTEXAI=\"$DEFAULT_FALSE_VALUE\"" \
            "GOOGLE_MODEL=\"$DEFAULT_MODEL_VALUE\"" \
            "DEFAULT_PROMPT=\"$DEFAULT_PROMPT_VALUE\"" \
            "GOOGLE_API_KEY=\"$DEFAULT_VALUE\"" \
            > "$ENV_FILE"
        warn "'.env' file created at $ENV_FILE"
        warn "Please update values for variables (and review LOAD_ flags) in '$ENV_FILE', then re-run this script."
        exit 0
    fi
}

# --- Ensure .env file has the basic structure (add missing lines with defaults, double-quoted in file) ---
ensure_env_structure() {
    local structure_changed=false
    # Mandatory Variables
    if ! grep -q "^GOOGLE_GENAI_USE_VERTEXAI=" "$ENV_FILE"; then
        info "Adding missing 'GOOGLE_GENAI_USE_VERTEXAI=\"$DEFAULT_FALSE_VALUE\"' to '$ENV_FILE'."
        echo "GOOGLE_GENAI_USE_VERTEXAI=\"$DEFAULT_FALSE_VALUE\"" >> "$ENV_FILE"; structure_changed=true
    fi
    if ! grep -q "^GOOGLE_MODEL=" "$ENV_FILE"; then
        info "Adding missing 'GOOGLE_MODEL=\"$DEFAULT_MODEL_VALUE\"' to '$ENV_FILE'."
        echo "GOOGLE_MODEL=\"$DEFAULT_MODEL_VALUE\"" >> "$ENV_FILE"; structure_changed=true
    fi
    if ! grep -q "^DEFAULT_PROMPT=" "$ENV_FILE"; then # New DEFAULT_PROMPT check
        info "Adding missing 'DEFAULT_PROMPT=\"$DEFAULT_PROMPT_VALUE\"' to '$ENV_FILE'."
        echo "DEFAULT_PROMPT=\"$DEFAULT_PROMPT_VALUE\"" >> "$ENV_FILE"; structure_changed=true
    fi
    if ! grep -q "^GOOGLE_API_KEY=" "$ENV_FILE"; then
        info "Adding missing 'GOOGLE_API_KEY=\"$DEFAULT_VALUE\"' to '$ENV_FILE'."
        echo "GOOGLE_API_KEY=\"$DEFAULT_VALUE\"" >> "$ENV_FILE"; structure_changed=true
    fi

    # Optional Sections and their LOAD flags/variables
    for section_def_string in "${SECTIONS_DEF[@]}"; do
        IFS=';' read -r _ load_flag_name _ <<< "$section_def_string" # Get only load_flag_name first
        
        # Ensure LOAD flag exists, default to "Y" (quoted) if missing
        if ! grep -q "^${load_flag_name}=" "$ENV_FILE"; then
            info "Adding missing '$load_flag_name=\"Y\"' to '$ENV_FILE'."
            echo "${load_flag_name}=\"Y\"" >> "$ENV_FILE"; structure_changed=true
        fi
        
        # Parse again for all variables in the section
        IFS=';'
        arr_parts=($section_def_string)
        unset IFS
        for ((i=2; i<${#arr_parts[@]}; i++)); do # Iterate over actual variables in the section
            var_name_to_check="${arr_parts[$i]}"
            if ! grep -q "^${var_name_to_check}=" "$ENV_FILE"; then
                info "Adding missing '$var_name_to_check=\"$DEFAULT_VALUE\"' to '$ENV_FILE'."
                echo "${var_name_to_check}=\"$DEFAULT_VALUE\"" >> "$ENV_FILE"; structure_changed=true
            fi
        done
    done

    if [ "$structure_changed" = true ]; then
        warn "The structure of '$ENV_FILE' was updated with default values for missing entries. Please review them and re-run the script if necessary."
    fi
}

# --- Validate .env file content ---
validate_env_vars() {
    local needs_update=false
    local vars_to_update_message="Please update the following variables in '$ENV_FILE':"

    # Validate MANDATORY GOOGLE_API_KEY
    local google_api_key_val
    google_api_key_val=$(get_env_var_value "GOOGLE_API_KEY") # Gets value with quotes stripped
    if [ -z "$google_api_key_val" ] || [ "$google_api_key_val" = "$DEFAULT_VALUE" ]; then
        vars_to_update_message+="\n- GOOGLE_API_KEY (is '$DEFAULT_VALUE' or missing - Mandatory)"
        needs_update=true
    fi
    # GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_MODEL, and DEFAULT_PROMPT are not checked against NOT_SET;
    # their presence and default values are ensured.

    # Validate Optional Sections based on their LOAD flags
    for section_def_string in "${SECTIONS_DEF[@]}"; do
        IFS=';'
        arr_parts=($section_def_string) 
        unset IFS
        
        local section_name_label="${arr_parts[0]}" 
        local load_flag_var_name="${arr_parts[1]}"
        local load_flag_value
        load_flag_value=$(get_env_var_value "$load_flag_var_name") # Gets value with quotes stripped

        if [ -z "$load_flag_value" ]; then 
            vars_to_update_message+="\n- $load_flag_var_name (is empty for $section_name_label section, must be Y or N)"
            needs_update=true
        elif [[ "$load_flag_value" == "Y" || "$load_flag_value" == "y" ]]; then
            for ((i=2; i<${#arr_parts[@]}; i++)); do 
                local var_name_to_check="${arr_parts[$i]}"
                local var_value
                var_value=$(get_env_var_value "$var_name_to_check") # Gets value with quotes stripped
                if [ -z "$var_value" ] || [ "$var_value" = "$DEFAULT_VALUE" ]; then
                    vars_to_update_message+="\n- $var_name_to_check (is '$DEFAULT_VALUE' or missing - required because $load_flag_var_name is Y for $section_name_label)"
                    needs_update=true
                fi
            done
        elif [[ "$load_flag_value" != "N" && "$load_flag_value" != "n" ]]; then 
             vars_to_update_message+="\n- $load_flag_var_name (for $section_name_label must be Y or N, currently '$load_flag_value')"
             needs_update=true
        fi
    done

    if [ "$needs_update" = true ]; then
        warn "$vars_to_update_message"
        exit 0 
    fi
}

# --- Main Script Logic ---

# 1. Create .env if it doesn't exist (also creates parent directory if needed)
create_env_file_if_not_exists

# 2. .env file exists, ensure its structure (add missing lines with defaults)
info "Found '$ENV_FILE'. Ensuring its structure..."
ensure_env_structure

# 3. Validate variable values based on LOAD flags
info "Validating variable values in '$ENV_FILE'..."
validate_env_vars

# 4. All checks passed. Source .env, display active config, and run command
info "All required variables are set according to LOAD flags."
info "Active configuration (values are masked where appropriate):"

# Source the .env file to load variables into the current shell's environment.
# When sourcing a file like VAR="value", bash assigns 'value' (unquoted) to VAR.
set -a
# shellcheck source=.env
source "$ENV_FILE"
set +a

# Display MANDATORY (already sourced)
echo "  Section: MANDATORY"
# Values from 'source' will be unquoted if they were quoted in the file.
gguv_val=$(eval echo "\$GOOGLE_GENAI_USE_VERTEXAI") 
gm_val=$(eval echo "\$GOOGLE_MODEL") 
dp_val=$(eval echo "\$DEFAULT_PROMPT") # New DEFAULT_PROMPT
ga_val=$(eval echo "\$GOOGLE_API_KEY")
echo "    GOOGLE_GENAI_USE_VERTEXAI: $(mask_value "$gguv_val")"
echo "    GOOGLE_MODEL: $(mask_value "$gm_val")"
echo "    DEFAULT_PROMPT: $(mask_value "$dp_val")" # Display new prompt
echo "    GOOGLE_API_KEY: $(mask_value "$ga_val")"

# Display Optional Sections if loaded (values are from sourced .env)
for section_def_string in "${SECTIONS_DEF[@]}"; do
    IFS=';'
    arr_parts=($section_def_string)
    unset IFS

    section_name_label="${arr_parts[0]}"
    load_flag_var_name="${arr_parts[1]}"
    
    load_flag_value_from_env=$(eval echo "\$$load_flag_var_name") 

    if [[ "$load_flag_value_from_env" == "Y" || "$load_flag_value_from_env" == "y" ]]; then
        echo "  Section: $section_name_label (LOADED)"
        echo "    $load_flag_var_name: $load_flag_value_from_env"
        for ((i=2; i<${#arr_parts[@]}; i++)); do
            var_name_to_display="${arr_parts[$i]}"
            value_from_env=$(eval echo "\$$var_name_to_display")
            echo "    $var_name_to_display: $(mask_value "$value_from_env")"
        done
    else
        echo "  Section: $section_name_label (NOT LOADED - $load_flag_var_name is '$load_flag_value_from_env')"
    fi
done

echo "" 
info "Attempting to run 'adk web' with the above configuration..."
echo "----------------------------------------------------------------------"

adk web

echo "----------------------------------------------------------------------"
info "'adk web' command finished."
