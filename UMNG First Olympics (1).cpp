#include <iostream>
using namespace std;

int main(void){
    int c=0;
    char arr[]={'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
    string word="", alph="";
    cin>>word>>alph;
    for (size_t i = 0; word[i]!='\0'; i++)
    {
        c=0;
        for (size_t j = 0; word[i]!=alph[j] ; j++)
            c++;
        word[i]=arr[c];
    }
    cout<<word;
    return 0;
}