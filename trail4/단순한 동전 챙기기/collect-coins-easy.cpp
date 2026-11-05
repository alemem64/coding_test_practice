#include <bits/stdc++.h>
using namespace std;

struct Node {
    int value;
    int r;
    int c;

    Node(int value, int r, int c) : value(value), r(r), c(c) {}
};
bool cmp(const Node& a, const Node& b) {
    return a.value<b.value;
}
int ans = INT_MAX;
int N;
vector<vector<char>> grid;
vector<Node> Nodes;
int startRow, startCol;
int endRow, endCol;

int GetDist(int x1, int y1, int x2, int y2) {
    return abs(x1-x2) + abs(y1-y2);
}

bool Check(int i, int j, int k) {
    int mini = Nodes[i].value;
    int midium = Nodes[j].value;
    int maxx = Nodes[k].value;

    if(mini>=midium || mini>=maxx || midium >= maxx) {
        return false;
    }
    return true;
}

int main() {
    // 입력
    cin >> N;
    grid.resize(N,vector<char>(N));
    // 시작, 도착점 row/col 기록
    // struct배열에 value, row/col 기록
    for(int i=0;i<N;i++) {
        for(int j=0;j<N;j++) {
            char tmp;
            cin >> tmp;
            grid[i][j] = tmp;

            if(isdigit(tmp)) {
                Nodes.push_back(Node(tmp-'0', i, j));
            }

            if(tmp=='S') {
                startRow = i;
                startCol = j;
            }

            if(tmp=='E') {
                endRow = i;
                endCol = j;
            }
        }
    }

    // 최적화: struct배열 크기 3보다 작으면 -1 출력+종료
    if(Nodes.size() < 3) {
        cout << -1;
        exit(0);
    }

    // struct배열 value 기준 오름차순 정렬
    sort(Nodes.begin(), Nodes.end(), cmp);

    int len = Nodes.size();
    // 3중 for문 완탐(struct 배열 인덱스)
    for(int i=0;i<len-2;i++) {
        for(int j=i+1;j<len-1;j++) {
            for(int k=j+1;k<len;k++) {
                int sum = 0;
                // 증가하는 번호 3개인지 체크
                if(!Check(i,j,k)) {
                    continue;
                }
                // 각 지점 순서대로 방문하는 '멘헤튼 거리' 합 + ans 갱신
                // S -> Nodes[i] -> Nodes[j] -> Nodes[k] -> E

                // S -> Nodes[i]
                sum += GetDist(startRow,startCol,Nodes[i].r,Nodes[i].c);
                // Nodes[i] -> Nodes[j]
                sum += GetDist(Nodes[i].r,Nodes[i].c,Nodes[j].r,Nodes[j].c);
                // Nodes[j] -> Nodes[k]
                sum += GetDist(Nodes[j].r,Nodes[j].c,Nodes[k].r,Nodes[k].c);
                // Nodes[k] -> E
                sum += GetDist(Nodes[k].r,Nodes[k].c,endRow,endCol);

                ans = min(ans,sum);   
            }
        }
    }

    if(ans==INT_MAX)
        cout << -1;
    else
        cout << ans;

    return 0;
}
