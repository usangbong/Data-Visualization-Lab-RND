using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoxMap : MonoBehaviour
{
    private int[,,] boxMap;

    public BoxMap()
    {
        boxMap = initMap();
    }

    private int[,,] initMap()
    {
        int[,,] map = new int[20,20,20];

        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
                for (int k = 0; k < 20; k++)
                    map[i, j, k] = 0;

        return map;
    }

    public int[,,] getBoxMap() { return boxMap; }

    public void fillMap(Box box, int x, int z, int y)
    {
        for (int i = z; i < z + box.getWidth(); i++)
            for (int j = x; j < x + box.getDepth(); j++)
                for (int k = y; k < y + box.getHeight(); k++)
                    boxMap[i, j, k] = 1;
    }

    public int canBoxInstall(Box box, int x, int z, int y)
    {
        if (z + box.getWidth() > 20) return BoxAgent.OVER_THE_BOX;
        else if (x + box.getDepth() > 20) return BoxAgent.OVER_THE_BOX;
        else if (y + box.getHeight() > 20) return BoxAgent.OVER_THE_BOX;
      
        if(만약 공간이 없다면?)
            return BoxAgent.NO_SPACE;
        
        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++)
                for (int k = 0; k < 20; k++)
                    if (boxMap[i, j, k]) return BoxAgent.NO_SPACE;

        for (int i = z; i < z + box.getWidth(); i++)
            for (int j = x; j < x + box.getDepth(); j++)
                for (int k = y; k < y + box.getHeight(); k++)
                    if (boxMap[i, j, k] == 1) return BoxAgent.CANT_INSTALL_BOX;

        return BoxAgent.CAN_INSTALL_BOX;
    }

    private Vector3 getMaxSpace()
    {
        int cnt;
        Vector3 max = Vector3.zero;

        for (int i=0;i<20;i++)
            for(int j=0;j<20;j++)
                for(int k = 0; k < 20; k++)
                {

                }

        return max;
    }

    public void Clear()
    {
        boxMap = initMap();
    }
}
