using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;

public class OfficeArea : MonoBehaviour
{
    //OVER 열거형
    public enum OverState { NOT_OVER, OVER_RIGHT, OVER_LEFT, OVER_UP, OVER_DOWN };    

    //Cell의 개수 (가로, 세로)
    public int x_Count, z_Count;
    //Cell 크기 (가로, 세로)
    public static float x_Size, z_Size;

    //생성 Cell List
    List<List<Cell>> cells = new List<List<Cell>>();

    //Area의 max, min 좌표
    public static float minX = -12f;
    public static float maxX = 12f;
    public static float minZ = -7.5f;
    public static float maxZ = 7.5f;

    //Snap Agent List
    public List<SnapAgent> snapList = new List<SnapAgent>();

    //Decision을 완료한 Object의 개수
    [HideInInspector]
    public int decisionObjectCount;

    //Cell x_Count * z_Count개 생성
    private void Awake()
    {
        decisionObjectCount = 0;

        //Cell 크기 계산
        x_Size = (float)(maxX - minX) / x_Count;
        z_Size = (float)(maxZ - minZ) / z_Count;

        //Cell 생성
        for(int i=0;i<z_Count;i++)
        {
            cells.Add(new List<Cell>());
            for(int j=0;j<x_Count;j++)
            {
                //index (0~39), x, z의 가운데 좌표
                Cell cell = new Cell(i * x_Count + j, (minX + x_Size / 2) + (j * x_Size), (maxZ - z_Size / 2) - (i * z_Size));
                cells[i].Add(cell);
            }
        }

        CellReset();
    }

    //Return All Cell List
    public List<List<Cell>> getAllCells() { return cells; }

    //Cell List Reset
    public void CellReset()
    {
        for(int i=0;i<z_Count;i++)
        {
            for(int j=0;j<x_Count;j++)
            {
                Cell cell = cells[i][j];
                cell.Clear();
            }
        }
    }

    //index에 해당하는 Cell 검색
    public Cell FindCellByIndex(int idx)
    {
        for (int i=0;i<z_Count;i++)
        {
            for(int j=0;j<x_Count;j++)
            {
                if (cells[i][j].getIdx() == idx) return cells[i][j];
            }
        }

        return null;
    }
    
    //Over된 Cell을 찾아서 그 Cell에 Object 추가
    public void SearchOverTheCellObjectAndAddObjectToCell(Cell cell, GameObject obj)
    {
        //길이 설정
        ObjectConfig config = obj.GetComponent<ObjectConfig>();
        float horizontalLength = config.getHorizontalLength();
        float verticalLength = config.getVerticalLength();

        //인덱스
        int idx = cell.getIdx();

        //x와 z방향으로 몇개의 Cell을 넘어갔는지 체크
        int x_cnt = (int)(horizontalLength / x_Size);
        int z_cnt = (int)(verticalLength / z_Size);

        //x축 방향으로 Over된 cell 검색
        Cell tempCell;
        for(int i=0;i<x_cnt;i++)
        {
            //오른쪽을 넘어가지 않았다면
            if(!cell.isOverObject(obj, (int)OverState.OVER_RIGHT))
            {
                tempCell = FindCellByIndex(idx + 1 * (i + 1));
                tempCell.AddObject(obj);
            }

            //왼쪽을 넘어가지 않았다면
            if(!cell.isOverObject(obj, (int)OverState.OVER_LEFT))
            {
                tempCell = FindCellByIndex(idx - 1 * (i + 1));
                tempCell.AddObject(obj);
            }
        }

        //z축 방향으로 Over된 cell 검색
        for(int j=0;j<z_cnt;j++)
        {
            //위쪽을 넘어가지 않았다면
            if (!cell.isOverObject(obj, (int)OverState.OVER_UP))
            {
                tempCell = FindCellByIndex(idx - x_Count * (j + 1));
                tempCell.AddObject(obj);
            }

            //아래쪽을 넘어가지 않았다면
            if(!cell.isOverObject(obj, (int)OverState.OVER_DOWN))
            {
                tempCell = FindCellByIndex(idx + x_Count * (j + 1));
                tempCell.AddObject(obj);
            }
        }

        decisionObjectCount++;
    }

    //중복 있는 Agent 찾아서 감점
    public void FindDuplicateCellAndDeductionToObject()
    {
        List<GameObject> objList;

        for (int i = 0; i < z_Count; i++)
        {
            for (int j = 0; j < x_Count; j++)
            {
                //Cell의 object개수가 2개 이상이면
                if (cells[i][j].getObjectCount() > 1)
                {
                    //List를 받아와서
                    objList = cells[i][j].getObjectList();

                    //List에 존재하는 모든 Object의 Agent에 1점 감점
                    for (int k = 0; k < objList.Count; k++)
                    {
                        Transform parent = objList[k].transform.parent;
                        Transform agent = parent.GetChild(1);
                        agent.GetComponent<CellAgent>().AddReward(-1f);
                    }
                }
            }
        }
    }

    //수평방향 Snap여부 검사
    public bool isHorizontalSnap(int idx)
    {
        if (idx >= 0 && idx <= x_Count - 1) return true;
        else if (idx >= (x_Count * z_Count) - x_Count && idx <= (x_Count * z_Count) - 1) return true;
        else return false;
    }

    //수직방향 Snap여부 검사
    public bool isVerticalSnap(int idx)
    {
        if (idx % x_Count == 0) return true;
        else if (idx % x_Count == x_Count - 1) return true;
        else return false;
    }

    float time = 0;
    private void FixedUpdate()
    {
        if (decisionObjectCount == 4)
        {
            FindDuplicateCellAndDeductionToObject();

            CellReset();

            for (int i = 0; i < 4; i++)
            {
                snapList[i].RequestDecision();
            }

            decisionObjectCount = 0;
        }
    }
}