using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OfficeArea : MonoBehaviour
{
    public int x_Count, z_Count;
    float x_diff, z_diff;

    //Delete
    public GameObject tempObj;

    Cell[,] cells = new Cell[5,8];

    const float minX = -12f;
    const float maxX = 12f;
    const float minZ = -7.5f;
    const float maxZ = 7.5f;

    private void Start()
    {
        x_diff = (float)(maxX - minX) / x_Count;
        z_diff = (float)(maxZ - minZ) / z_Count;

        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                cells[i, j] = new Cell((i + 1) * (j + 1) - 1, (minX + x_diff / 2) + (j * x_diff), (maxZ - z_diff / 2) - (i * z_diff), Instantiate(tempObj)); //tempObj delete
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

    public int FIndCellIndex(Cell cell)
    {
        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                if (cells[i, j] == cell) return cells[i, j].getIdx();
            }
        }

        return -1;
    }

    public void DeductionToAgent()
    {
        List<GameObject> agentList;

        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                if (cells[i, j].getAgentCount() > 1)
                {
                    agentList = cells[i, j].getAgentList();

                    for (int k = 0; k < agentList.Count; k++)
                    {
                        agentList[k].GetComponent<OfficeAgent>().AddReward(-1f * cells[i, j].getAgentCount());
                    }
                }
            }
        }
    }

    public void AddObject(Cell cell, GameObject agent)
    {
        cell.AddObject(agent);

        ObjectConfig config = agent.GetComponent<ObjectConfig>();
        int xLen = (int)(config.x_Length / x_diff);
        int zLen = (int)(config.y_Length / z_diff);

        int idx = FIndCellIndex(cell);

        Cell tempCell;
        for (int i = 0; i < xLen; i++)
        {
            tempCell = FindCell(idx + 1);
            tempCell.AddObject(agent);

            tempCell = FindCell(idx - 1);
            tempCell.AddObject(agent);
        }

        for (int i = 0; i < zLen; i++)
        {
            tempCell = FindCell(idx + z_Count);
            tempCell.AddObject(agent);

            tempCell = FindCell(idx - z_Count);
            tempCell.AddObject(agent);
        }
    }
}