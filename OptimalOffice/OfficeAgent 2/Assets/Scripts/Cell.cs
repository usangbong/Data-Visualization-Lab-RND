using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cell : MonoBehaviour
{
    int idx;
    Vector3 minPos, maxPos, centerPos;
    List<GameObject> agentList;
    //Delete
    GameObject tempObj;

    public Cell(int _idx, float c_x, float c_z, GameObject _temp) //_temp Delete
    {
        idx = _idx;

        agentList = new List<GameObject>();

        minPos.x = c_x - 1.5f;
        minPos.z = c_z - 1.5f;

        maxPos.x = c_x + 1.5f;
        maxPos.z = c_z + 1.5f;

        minPos.y = maxPos.y = 0f;

        centerPos = (minPos + maxPos) / 2.0f;

        //Delete
        tempObj = _temp;
        tempObj.transform.position = centerPos;
    }

    public int getIdx() { return idx; }
    public int getAgentCount() { return agentList.Count; }
    public List<GameObject> getAgentList() { return agentList; }

    public Vector3 getMinPos() { return minPos; }
    public Vector3 getMaxPos() { return maxPos; }
    public Vector3 getCenterPos() { return centerPos; }

    public Vector3 AddObject(GameObject agent) 
    { 
        agentList.Add(agent);
        return centerPos;
    }
}
