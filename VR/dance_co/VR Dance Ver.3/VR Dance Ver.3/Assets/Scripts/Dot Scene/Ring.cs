using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ring : MonoBehaviour
{
    public GameObject Rings;
    public int cnt;
    public bool colorFull, ringFinish;

    Circle circle;
    bool ringActive;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
        Rings.SetActive(false);
        ringActive = colorFull = ringFinish = false;
        cnt = 0;
    }
     
    void Update()
    {
        if (!circle.isSize && circle.sizeStart)
        {
            if(!ringActive)
            {
                Rings.SetActive(true);
                ringActive = true;
            }
        }

        Rings.transform.Rotate(Vector3.down * 90f * Time.deltaTime);

        if (cnt == 20)
        {
            colorFull = true;
        }

        if (!circle.isBlinking && !ringFinish)
        {
            Rings.transform.position = Vector3.MoveTowards(Rings.transform.position,
                new Vector3(1.3f, 1f, 0), 0.5f * Time.deltaTime);
            Rings.transform.rotation = Quaternion.Slerp(Rings.transform.rotation,
                Quaternion.Euler(90f, 90f, 0), 1.0f * Time.deltaTime);

            if(Rings.transform.position == new Vector3(1.3f, 1f, 0))
            {
                ringFinish = true;
            }
        }
    }
}
