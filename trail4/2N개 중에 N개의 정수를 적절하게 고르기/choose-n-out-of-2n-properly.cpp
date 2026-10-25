#include <iostream>
#include <algorithm>
#include <vector>
#include <climits>

using namespace std;

int ans = INT_MAX;
int n;
int total;
vector<int>nums;
vector<int>v;

void sol(int level,int before){
    if(level>=n){
        int cur = 0;
        for(int i = 0; i<v.size(); i++){
            // cout << v[i] << " ";
            cur += v[i];
        }
        // cout << endl;

        int tmp = abs((total-cur)-cur);
        ans = min(tmp,ans);

        return;
    }

    for(int i = before+1; i<nums.size(); i++){
        v.push_back(nums[i]);
        sol(level+1,i);
        v.pop_back();
    }
}

int main() {
    cin >> n;

    int a;
    for(int i = 0; i<2*n; i++){
        cin >> a;
        total+=a;
        nums.push_back(a);
    }

    sol(0,-1);

    cout << ans;
}
