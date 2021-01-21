using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridInformation : MonoBehaviour
{
    public Transform gridParent;

    List<List<Cell>> grid;
    List<List<int>> map;

    private void Awake()
    {
        grid = new List<List<Cell>>();
        map = new List<List<int>>();

        for (var i = 0; i < gridParent.childCount; i++)
        {
            map.Add(new List<int>());
            grid.Add(new List<Cell>());

            for(var j=0;j<gridParent.GetChild(i).childCount;j++)
            {
                grid[i].Add(gridParent.GetChild(i).GetChild(j).GetComponent<Cell>());
            }
        }

        initializeMap();
    }

    private void Start()
    {
        
    }

    public void setMap(List<Cell> markingCell)
    {
        
    }

    public List<Cell> getPath(Cell startNode, Cell endNode)
    {
        List<Cell> path = new List<Cell>();

        return path;
    }

    public float extractDistance(List<Cell> path)
    {
        float distance = 0;

        return distance;
    }

    public void initializeMap()
    {
        for(var i=0;i<grid.Count;i++)
        {
            for(var j=0;j<grid[i].Count;j++)
            {
                map[i][j] = 0;
                grid[i][j].removeObject();
            }
        }
    }
}
