using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OfficeArea : MonoBehaviour
{
    const float maxX = 12f;
    const float minX = -12f;
    const float maxZ = 7.5f;
    const float minZ = -7.5f;

    private void Start()
    {
        AreaReset();
    }

    public void AreaReset()
    {
        transform.position = new Vector3(getPos(minX, maxX), transform.position.y, getPos(minZ, maxZ));
        transform.rotation = Quaternion.Euler(new Vector3(0, getRot(), 0));
    }

    float getPos(float min, float max)
    {
        float pos = Random.Range(min, max);

        pos = Mathf.Round(pos * 10) / 10;

        return pos;
    }

    float getRot()
    {
        int i = Random.Range(0, 4);

        switch(i)
        {
            case 0: return 0;
            case 1: return 90;
            case 2: return 180;
            case 3: return 270;
            default: return -1;
        }
    }
}
