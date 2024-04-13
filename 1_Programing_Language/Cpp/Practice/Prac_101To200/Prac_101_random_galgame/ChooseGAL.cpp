#include <iostream>
#include <filesystem>
#include <fstream>

#include <map>
#include <vector>
#include <string>

#include <random>
#include <ctime>

using std::cout;
using std::endl;
using std::cin;

using std::ifstream;
using std::ofstream;

using std::map;
using std::string;
using std::vector;
using std::filesystem::directory_iterator;

int main() {

    // check if the .kobayashi_gal_config exists
    // if not, create it, and let user input a deafault gal_folder
    // if exists, give a default choose, and let user choose

    string GAL_FOLDER = "";

    if (!std::filesystem::exists(".kobayashi_gal_config")) {
        ofstream ofs(".kobayashi_gal_config");
        ofs.close();
    } else {
        ifstream ifs(".kobayashi_gal_config");
        ifs >> GAL_FOLDER;
        ifs.close();
    }

    if (GAL_FOLDER.empty()) {
        ofstream ofs(".kobayashi_gal_config");
        cout << "Please input the gal folder: ";
        getline(cin, GAL_FOLDER);
        // check if the folder exists
        while (!std::filesystem::exists(GAL_FOLDER)) {
            cout << "The folder [" << GAL_FOLDER << "] does not exist, please input again: ";
            cin >> GAL_FOLDER;
        }
        ofs << GAL_FOLDER;
        ofs.close();
    } else {
        cout << "The gal folder is: " << GAL_FOLDER << endl;
        cout << "Press Enter to continue, or input a new gal folder: ";
        string gal_folder_temp;
        getline(cin, gal_folder_temp);
        if (!gal_folder_temp.empty()) {
            ofstream ofs(".kobayashi_gal_config");
            while (!std::filesystem::exists(gal_folder_temp)) {
                cout << "The folder [" << gal_folder_temp << "] does not exist, please input again: ";
                getline(cin, gal_folder_temp);
            }
            if (!gal_folder_temp.empty()) {
                GAL_FOLDER = gal_folder_temp;
                ofs << GAL_FOLDER;
            }
            ofs.close();
        }
    }

    // the first layer of folder is the company name
    // the second layer of folder is the galgame name

    map<string, vector<string>> gal_list; 

    for (auto& dir : directory_iterator(GAL_FOLDER)) {
        string company_name;
        string gal_name;
        company_name = dir.path().filename().string();
        vector<string> gal_names;
        for (auto& gal : directory_iterator(dir.path())) {
            gal_names.push_back(gal.path().filename().string());
        }
        gal_list[company_name] = gal_names;
    }

    // choose 5 galgames randomly
    std::default_random_engine e(time(0));
    std::uniform_int_distribution<unsigned> u(0, gal_list.size() - 1);

    vector<string> random_gal_list;
    short gal_count = 0;
    short repeat_count = 0;

    while (gal_count < 5) {
        int company_index = u(e);
        auto it = gal_list.begin();
        std::advance(it, company_index);
        string company_name = it->first;
        vector<string> gal_names = it->second;

        int gal_index = u(e) % gal_names.size();
        string gal_name = gal_names[gal_index];

        string company_gal = company_name + ":" + gal_name;
        if (std::find(random_gal_list.begin(), random_gal_list.end(), company_gal) == random_gal_list.end()) {
            random_gal_list.push_back(company_gal);
            gal_count++;
        } else {
            repeat_count++;
            if (repeat_count > 10) {
                cout << "There are not enough gals in the folder, please check the folder." << endl;
                break;
            }
        }
    }

    for (auto& gal : random_gal_list) {
        cout << gal << endl;
    }

    cout << "Press any key to exit...";
    cin.get();

    return 0;
}
