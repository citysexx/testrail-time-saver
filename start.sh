#!/usr/bin/env bash

function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;  
            [Nn]*) return 1  ;;
        esac
    done
}

function get_creds {

    read -p "Enter valid Testrail Url >>> " TESTRAIL_URL
    suf="/"
    httppre="http://"
    httpspre="https://"
    host=${TESTRAIL_URL#"$httppre"}
    host=${host#"$httpspre"}
    host=${host%"$suf"}
    if ping -c 4 $host; then
        echo info: service is available
    else
        echo error: service is not available
        exit 1
    fi

    read -p "Enter valid Testrail Email >>> " TESTRAIL_EMAIL

    unset PASSWORD
    unset CHARCOUNT

    echo -n "Enter password: "

    stty -echo

    CHARCOUNT=0
    while IFS= read -p "$PROMPT" -r -s -n 1 CHAR
    do
        # Enter - accept password
        if [[ $CHAR == $'\0' ]] ; then
            break
        fi
        # Backspace
        if [[ $CHAR == $'\177' ]] ; then
            if [ $CHARCOUNT -gt 0 ] ; then
                CHARCOUNT=$((CHARCOUNT-1))
                PROMPT=$'\b \b'
                PASSWORD="${PASSWORD%?}"
            else
                PROMPT=''
            fi
        else
            CHARCOUNT=$((CHARCOUNT+1))
            PROMPT='*'
            PASSWORD+="$CHAR"
        fi
    done

    stty echo

    echo "TESTRAIL_URL=$TESTRAIL_URL" > .env
    echo "TESTRAIL_EMAIL=$TESTRAIL_EMAIL" >> .env
    echo "TESTRAIL_PASSWORD=$PASSWORD" >> .env
}

python3 -m venv .venv
source ./.venv/bin/activate
echo Installing python packages with pip...
if pip install -r ./requirements.txt > /dev/null; then
    ENV_FILE="./.env"
    if test -f "$ENV_FILE"; then
        yes_or_no "Creds already exist. Do you want to rewrite them?" && rm .env && get_creds
    fi
    python3 main.py
else
    echo "Your pip output sucks. Please refer to the errors and fix them."
fi
