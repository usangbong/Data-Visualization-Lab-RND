using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class Flat : MonoBehaviour
{
    public GameObject flatCircle, tracker;
    bool a, b;
    ColorCircle cCircle;

    public bool isTime, moveStart;
    bool func;
    float len1, len2, len3;
    public float time;

    void Start()
    {
        flatCircle.SetActive(false);
        cCircle = GameObject.Find("ColorCircleManager").GetComponent<ColorCircle>();
        a = moveStart = b = false;
        time = 0.0f;
        isTime = true;
        func = false;
    }

    void Update()
    {           
        if (cCircle.move)
        {
            flatCircle.SetActive(true);
            if(!func)
            {
                StartCoroutine(timeChecker());
                func = true;
            }

            Invoke("MoveFlatCircle", 1.5f);
        }
    }

    void MoveFlatCircle()
    {
        moveStart = true;
    }

    float CalculateLen(Vector3 a, Vector3 b)
    {
        return Mathf.Sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) +
            (a.z - b.z) * (a.z - b.z));
    }

    IEnumerator timeChecker()
    {
        while(isTime)
        {
            time += 0.01f;

            if(time > 30f)
            {
                isTime = false;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }
}
