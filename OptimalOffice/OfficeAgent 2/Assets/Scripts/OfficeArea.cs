using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OfficeArea : MonoBehaviour
{
    public OfficeAgent agent;

    const float maxX = 12f;
    const float minX = -12f;
    const float maxZ = 7.5f;
    const float minZ = -7.5f;

    Cell[,] cells = new Cell[5,8];

    private void Start()
    {
        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                cells[i,j] = new Cell((i+1)*(j+1) - 1, -10.5f + j*3f, 6f - i*3f);
            }
        }
    }

    public Cell FindCell(int idx)
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

    public void DeductionToAgent()
    {
        List<GameObject> agentList;

        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                if(cells[i,j].getAgentCount() > 1)
                {
                    agentList = cells[i, j].getAgentList();

                    for(int k=0;k< agentList.Count;k++)
                    {
                        agentList[k].GetComponent<OfficeAgent>().AddReward(-1f * cells[i,j].getAgentCount());
                    }
                }
            }
        }
    }
}

public class Cell
{
    int idx;
    Vector2 minPos, maxPos;
    List<GameObject> agentList;

    public int getIdx() { return idx; }
    public int getAgentCount() { return agentList.Count; }
    public List<GameObject> getAgentList() { return agentList; }
    public Vector2 getMinPos() { return minPos; }
    public Vector2 getMaxPos() { return maxPos; }

    public Vector3 getObjectPos(GameObject agent)
    {
        Vector3 centerPos;

        centerPos.x = (minPos.x + maxPos.x) / 2.0f;
        centerPos.y = 0f;
        centerPos.z = (minPos.y + maxPos.y) / 2.0f;

        agentList.Add(agent);

        return centerPos;
    }

    public Cell(int _idx, float c_x, float c_y)
    {
        idx = _idx;

        agentList = new List<GameObject>();

        minPos.x = c_x - 1.5f;
        minPos.y = c_y - 1.5f;

        maxPos.x = c_x + 1.5f;
        maxPos.y = c_y + 1.5f;
    }
}