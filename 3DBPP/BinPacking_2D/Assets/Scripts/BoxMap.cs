using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoxMap
{
    private int[,] boxMap;
    private GameObject mapObj;

    private Color org, dest;

    public BoxMap(GameObject obj, Color c1, Color c2)
    {
        mapObj = obj;

        org = c1;
        dest = c2;

        boxMap = initMap();
    }

    private int[,] initMap()
    {
        int[,] map = new int[20,20];

        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
            {
                mapObj.transform.GetChild(i).GetChild(j).GetComponent<MeshRenderer>().material.color = org;
                map[i, j] = 0;
            }

        return map;
    }

    public int[,] getBoxMap() { return boxMap; }

    public void fillMap(MiddleBox box, int x, int z)
    {
        for (int i = z; i < z + box.getWidth(); i++)
            for (int j = x; j < x + box.getLength(); j++)
            {
                mapObj.transform.GetChild(j).GetChild(i).GetComponent<MeshRenderer>().material.color = dest;
                boxMap[i, j] = 1;
            }
    }

    public int canBoxInstall(MiddleBox box, int x, int z)
    {
        if (x + box.getLength() > 20) return BoxAgent.OVER_THE_BOX;
        if (z + box.getWidth() > 20) return BoxAgent.OVER_THE_BOX;

        if (!canMaxSpace(box)) return BoxAgent.NO_SPACE;

        for (int i = z; i < z + box.getWidth(); i++)
            for (int j = x; j < x + box.getLength(); j++)
                if (boxMap[i, j] == 1) return BoxAgent.CANT_INSTALL_BOX;

        return BoxAgent.CAN_INSTALL;
    }

    private bool canMaxSpace(MiddleBox box)
    {
        int m, n;

        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
            {
                if (i + box.getWidth() > 20 || j + box.getLength() > 20) continue;

                for (m = i; m < i + box.getWidth(); m++)
                {
                    for (n = j; n < j + box.getLength(); n++)
                        if (boxMap[m, n] == 1) break;

                    if (n != j + box.getLength()) break;
                }

                if (m == i + box.getWidth()) return true;
            }

        return false;
    }

    public void Clear()
    {
        boxMap = initMap();
    }
}
