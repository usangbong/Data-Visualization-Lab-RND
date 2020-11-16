using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player_Area : MonoBehaviour
{
    public int x_num;
    public int z_num;

    List<List<Player_Cell>> cellList;

    public static float minX = -12f;
    public static float maxX = 12f;
    public static float minZ = -7.5f;
    public static float maxZ = 7.5f;

    private float x_size, z_size;

    private void Awake()
    {
        cellList = new List<List<Player_Cell>>();

        x_size = (float)(maxX - minX) / x_num;
        z_size = (float)(maxZ - minZ) / z_num;
    }

    private void Start()
    {
        for (var i = 0; i < z_size; i++)
        {
            cellList.Add(new List<Player_Cell>());

            for (var j = 0; j < x_size; j++)
            {
                Player_Cell cell = new Player_Cell(i * x_num + j, (minX + x_size / 2) + (j * x_size), (maxZ - z_size / 2) - (i * z_size));
                cellList[i].Add(cell);
            }
        }
    }

    public Player_Cell findCell(GameObject obj)
    {
        for(var i=0;i<z_size;i++)
        {
            for(var j=0;j<x_size;j++)
            {
                Player_Cell cell = cellList[i][j];

                List<GameObject> objList = cell.getObjList();

                for(var k=0;k<objList.Count;k++)
                {
                    if (obj == objList[k]) return cell;
                }
            }
        }

        return null;
    }

    public Player_Cell getNextCell(Player_Cell cell, int where)
    {
        int idx = cell.getCellIndex();
        Player_Cell nextCell;

        switch(where)
        {
            case Info.RIGHT:
                nextCell = cellList[idx / x_num][idx % x_num + 1];
                break;
            case Info.LEFT:
                nextCell = cellList[idx / x_num][idx % x_num - 1];
                break;
            case Info.UP:
                nextCell = cellList[idx / x_num - 1][idx % x_num];
                break;
            case Info.DOWN:
                nextCell = cellList[idx / x_num + 1][idx % x_num];
                break;
            default:
                nextCell = null;
                break;
        }

        return nextCell;
    }
}
