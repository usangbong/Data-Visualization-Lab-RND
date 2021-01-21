using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Map : MonoBehaviour
{
    public Transform MapObj;

    private List<List<int>> map;
    private List<List<Transform>> mapObjList;

    private void Awake()
    {
        map = new List<List<int>>();
        mapObjList = new List<List<Transform>>();

        for (var i = 0; i < 12; i++)
        {
            map.Add(new List<int>());
            for (var j = 0; j < 12; j++)
            {
                map[i].Add(0);
            }
        }

        for (var i = 0; i < 12; i++)
        {
            mapObjList.Add(new List<Transform>());
            for (var j = 0; j < 12; j++)
            {
                mapObjList[i].Add(MapObj.GetChild(i).GetChild(j));
                mapObjList[i][j].GetComponent<MeshRenderer>().material.color = Color.white;
            }
        }
    }

    public void fillMap(int x, int z, int xSize, int zSize, Color color)
    {
        for (var i = z; i < z + zSize; i++)
        {
            for (var j = x; j < x + xSize; j++)
            {
                map[i][j] = 1;
                mapObjList[i][j].GetComponent<MeshRenderer>().material.color = color;
            }
        }
    }

    public bool canFillMap(int x, int z, int xSize, int zSize)
    {
        if (x + xSize > 12 || x < 0) return false;
        if (z + zSize > 12 || z < 0) return false;

        for (var i = z; i < z + zSize; i++)
        {
            for (var j = x; j < x + xSize; j++)
            {
                if (map[i][j] == 1) return false;
            }
        }

        return true;
    }    

    public void clearMap()
    {
        for (var i = 0; i < 12; i++)
        {
            for (var j = 0; j < 12; j++)
            {
                map[i][j] = 0;
                mapObjList[i][j].GetComponent<MeshRenderer>().material.color = Color.white;
            }
        }
    }

    public void deleteMap(int x, int z, int xSize, int zSize)
    {
        for (var i = z; i < z + zSize; i++)
        {
            for (var j = x; j < x + xSize; j++)
            {
                map[i][j] = 0;
                mapObjList[i][j].GetComponent<MeshRenderer>().material.color = Color.white;
            }
        }
    }
}
