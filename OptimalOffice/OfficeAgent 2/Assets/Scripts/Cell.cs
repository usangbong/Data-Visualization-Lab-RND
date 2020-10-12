﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cell : MonoBehaviour
{
    //Cell의 index
    int idx;
    //Cell의 최소 좌표, 최대 좌표, 가운데 좌표
    Vector3 minPos, maxPos, centerPos;
    //Cell에 존재하는 Object들의 List 생성
    List<GameObject> objList;

    //Delete
    public GameObject cellObj;

    //생성자
    public Cell(int _idx, float c_x, float c_z, GameObject _cell) // Delete, _cell
    {
        idx = _idx;

        objList = new List<GameObject>();

        //최소 좌표 생성
        minPos.x = c_x - 1.5f;
        minPos.z = c_z - 1.5f;

        //최대 좌표 생성
        maxPos.x = c_x + 1.5f;
        maxPos.z = c_z + 1.5f;

        minPos.y = maxPos.y = 0f;

        //중심 좌표 생성
        centerPos = (minPos + maxPos) / 2.0f;

        //Delete
        cellObj = _cell;
        cellObj.GetComponent<MeshRenderer>().material.color = Color.red;
    }

    public Vector3 getCenterPos() { return centerPos; }

    //index 반환
    public int getIdx() { return idx; }
    //Cell에 존재하는 object 개수 반환
    public int getObjectCount() { return objList.Count; }
    //Cell에 존재하는 object의 List 반환
    public List<GameObject> getObjectList() { return objList; }

    //Cell에 Object 추가
    public void AddObject(GameObject obj) { objList.Add(obj); }

    //Object가 지정된 길이를 초과하는지 검사
    public bool isOverObject(GameObject obj, int where)
    {
        //Object는 중심점을 기준으로 존재하므로 원래 길이 / 2
        ObjectConfig config = obj.GetComponent<ObjectConfig>();
        float horizontalLength = config.getHorizontalLength();
        float verticalLength = config.getVerticalLength();

        switch(where)
        {
            case (int)OfficeArea.OverState.OVER_RIGHT:
                if (centerPos.x + horizontalLength > OfficeArea.maxX) return true;
                break;
            case (int)OfficeArea.OverState.OVER_LEFT:
                if (centerPos.x - horizontalLength < OfficeArea.minX) return true;
                break;
            case (int)OfficeArea.OverState.OVER_UP:
                if (centerPos.z + verticalLength > OfficeArea.maxZ) return true;
                break;
            case (int)OfficeArea.OverState.OVER_DOWN:
                if (centerPos.z - verticalLength < OfficeArea.minZ) return true;
                break;
        }

        if(where == (int)OfficeArea.OverState.NOT_OVER) return true;
        else return false;
    }
}
