﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OfficeArea : MonoBehaviour
{
    public enum OverState { NOT_OVER, OVER_RIGHT, OVER_LEFT, OVER_UP, OVER_DOWN };    

    //Cell의 개수 (가로, 세로)
    public int x_Count, z_Count;
    //Cell 크기 (가로, 세로)
    public static float x_Size, z_Size;

    //Delete
    public GameObject tempObj;

    //생성 Cell List
    Cell[,] cells = new Cell[5,8];

    //Area의 max, min 좌표
    public static float minX = -12f;
    public static float maxX = 12f;
    public static float minZ = -7.5f;
    public static float maxZ = 7.5f;

    //Cell x_Count * z_Count개 생성
    private void Start()
    {
        //Cell 크기 계산
        x_Size = (float)(maxX - minX) / x_Count;
        z_Size = (float)(maxZ - minZ) / z_Count;

        //Cell 생성
        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                //index (0~39), x, z의 가운데 좌표
                cells[i, j] = new Cell((i + 1) * (j + 1) - 1, (minX + x_Size / 2) + (j * x_Size), (maxZ - z_Size / 2) - (i * z_Size), Instantiate(tempObj)); //tempObj delete
            }
        }
    }

    //index에 해당하는 Cell 검색
    public Cell FindCellByIndex(int idx)
    {
        for (int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                if (cells[i, j].getIdx() == idx) return cells[i, j];
            }
        }

        return null;
    }
    
    public void SearchOverTheCellObjectAndAddObjectToCell(Cell cell, GameObject obj)
    {
        ObjectConfig config = obj.GetComponent<ObjectConfig>();
        float horizontalLength = config.getHorizontalLength();
        float verticalLength = config.getVerticalLength();

        int idx = cell.getIdx();

        int x_count = (int)(horizontalLength / x_Size);
        int y_count = (int)(verticalLength / z_Size);

        Cell tempCell;
        for(int i=0;i<x_count;i++)
        {
            if(cell.isOverObject(obj) != (int)OverState.OVER_RIGHT)
            {
                tempCell = FindCellByIndex(idx + 1 * (i + 1));
                tempCell.AddObject(obj);
            }

            if(cell.isOverObject(obj) != (int)OverState.OVER_LEFT)
            {
                tempCell = FindCellByIndex(idx - 1 * (i + 1));
                tempCell.AddObject(obj);
            }
        }

        for(int j=0;j<y_count;j++)
        {
            if(cell.isOverObject(obj) != (int)OverState.OVER_UP)
            {
                tempCell = FindCellByIndex(idx - 8 * (j + 1));
                tempCell.AddObject(obj);
            }

            if(cell.isOverObject(obj) != (int)OverState.OVER_DOWN)
            {
                tempCell = FindCellByIndex(idx + 8 * (j + 1));
                tempCell.AddObject(obj);
            }
        }
    }

    //중복 있는 Agent 찾아서 감점
    public void FindDuplicateCellAndDeductionToObject()
    {
        List<GameObject> objList;

        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                //Cell의 object개수가 2개 이상이면
                if (cells[i, j].getObjectCount() > 1)
                {
                    //List를 받아와서
                    objList = cells[i, j].getObjectList();

                    //List에 존재하는 모든 Object의 Agent에 1점 감점
                    for (int k = 0; k < objList.Count; k++)
                    {
                        objList[k].GetComponent<OfficeAgent>().AddReward(-1f);
                    }
                }
            }
        }
    }
}