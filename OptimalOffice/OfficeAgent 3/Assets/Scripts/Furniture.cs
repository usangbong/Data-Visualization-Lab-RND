using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Furniture : MonoBehaviour
{
    /*public Vector2 centerPos;
    public float width, length;
    private Vector2[] corners;

    private void Awake()
    {
        corners = new Vector2[4];

        corners[0] = new Vector2(centerPos.x - width / 2, centerPos.y - length / 2);
        corners[1] = new Vector2(centerPos.x + width / 2, centerPos.y - length / 2);
        corners[2] = new Vector2(centerPos.x - width / 2, centerPos.y + length / 2);
        corners[3] = new Vector2(centerPos.x + width / 2, centerPos.y + length / 2);
    }

    public Vector2 findCloseCornersByEnv(Vector2[] envCorners)
    {
        Vector2 minPos = new Vector2(0, 0);
        float minDistance = 10000;

        for(int i=0;i<4;i++)
        {
            Vector2 pos = new Vector2(gameObject.transform.position.x, gameObject.transform.position.z);
            //float distance = Vector2.Distance(gameObject.transform.position);
        }
    }

    public Vector2 minDistanceCorner(Vector2 cornerPos)
    {
        Vector2 minPos = new Vector2(0, 0);
        float minDistance = 10000;

        for (int i=0;i<4;i++)
        {
            float distance = Vector2.Distance(cornerPos, corners[i]);

            if (distance < minDistance)
            {
                minDistance = distance;
                minPos = corners[i];
            }
        }

        return minPos;
    }

    void Start()
    {
        
    }
    void Update()
    {
        
    }*/
}
