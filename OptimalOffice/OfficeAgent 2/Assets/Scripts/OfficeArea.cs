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
                cells[i,j] = new Cell((i+1)*(j+1), -10.5f + j*3f, 6f - i*3f);
            }
        }
    }
}

class Cell
{
    int idx;
    Vector2 minPos, maxPos;

    public Vector2 getMinPos() { return minPos; }
    public Vector2 getMaxPos() { return maxPos; }

    public Cell(int _idx, float c_x, float c_y)
    {
        idx = _idx;

        minPos.x = c_x - 1.5f;
        minPos.y = c_y - 1.5f;

        maxPos.x = c_x + 1.5f;
        maxPos.y = c_y + 1.5f;
    }
}
