#! /usr/bin/env bash

#--------[ Colors ]------------------------------------------------------------
Green='\033[0;32m'
Red='\033[0;31m'
Blue='\033[0;34m'
BBlue='\033[1;34m'
BWhite='\033[1;37m'
NC='\033[m'

#--------[ pull_full_state_data ]----------------------------------------------
function pull_full_state_data()
{
    url='https://covidtracking.com/api/v1/states/daily.json'
    filename='all-states-daily.json'
    tmp_file=".$filename.tmp"
    
    echo -e "    ${Blue}[i]${NC} URL: $url"
    echo -e "    ${Blue}[i]${NC} Data File: $filename"
    echo -en "    ${NC}[ ] Pulling data for all states${NC}"
    curl -s $url > "$tmp_file"
    retval=$?
    if (( $retval != 0 ));then
        echo -e "\r    ${Red}[X]${NC} "
        exit
    else
        echo -e "\r    ${Green}[*]${NC} "
    fi


    echo -en "    ${NC}[ ] Check if data has changed${NC}"
    curr_sha=$(shasum $filename | cut -d " " -f1)
    new_sha=$(shasum $tmp_file | cut -d " " -f1)
    echo -e "\r    ${Green}[*]${NC}"

    if [ "$curr_sha" == "$new_sha" ]; then
       echo -e "    ${Blue}[i]${NC} No chage in data"
       rm $tmp_file
    else
        echo -en "    ${NC}[ ] Back up old data${NC}"
        mv -f "$filename" "$filename.bak"
        echo -e "\r    ${Green}[*]${NC}"

        echo -en "    ${NC}[ ] Save new data${NC}"
        mv -f "$tmp_file" "$filename"
        echo -e "\r    ${Green}[*]${NC}"
    fi
}

#--------[ pull_country_data ]-------------------------------------------------
function pull_country_data()
{
    url='https://covidtracking.com/api/us/daily'
    filename='country-daily.json'
    tmp_file=".$filename.tmp"
    
    echo -e "    ${Blue}[i]${NC} URL: $url"
    echo -e "    ${Blue}[i]${NC} Data File: $filename"
    echo -en "    ${NC}[ ] Pulling data United States${NC}"
    curl -s $url > "$tmp_file"
    retval=$?
    if (( $retval != 0 ));then
        echo -e "\r    ${Red}[X]${NC} "
        exit
    else
        echo -e "\r    ${Green}[*]${NC} "
    fi

    echo -en "    ${NC}[ ] Check if data has changed${NC}"
    curr_sha=$(shasum $filename | cut -d " " -f1)
    new_sha=$(shasum $tmp_file | cut -d " " -f1)
    echo -e "\r    ${Green}[*]${NC}"

    if [ "$curr_sha" == "$new_sha" ]; then
       echo -e "    ${Blue}[i]${NC} No chage in data"
       rm $tmp_file
    else
        echo -en "    ${NC}[ ] Back up old data${NC}"
        mv -f "$filename" "$filename.bak"
        echo -e "\r    ${Green}[*]${NC}"

        echo -en "    ${NC}[ ] Save new data${NC}"
        mv -f "$tmp_file" "$filename"
        echo -e "\r    ${Green}[*]${NC}"
    fi
}

#--------[ Main ]--------------------------------------------------------------
echo '+=========================================+'
echo '|    Pulling United States COVID Data     |'
echo '+=========================================+'

echo -e "${BBlue}[I]${NC} ${BWhite}Pulling data for all states${NC}"
pull_full_state_data

echo -e "${BBlue}[I]${NC} ${BWhite}Pulling data for country${NC}"
pull_country_data



