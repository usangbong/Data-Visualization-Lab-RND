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

    private void Start()
    {
        
    }

    public void AreaReset()
    {
        transform.position = new Vector3(getPos(minX, maxX), transform.position.y, getPos(minZ, maxZ));
    }

    float getPos(float min, float max)
    {
        float pos = Random.Range(min, max);

        pos = Mathf.Round(pos * 10) / 10;

        return pos;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "moveObject")
        {
            agent.collidingOtherObject();
        }
    }
}
