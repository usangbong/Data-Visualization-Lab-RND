using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorFiercing : MonoBehaviour
{
    public GameObject c1, c2, c3;
    public GameObject tmp;

    public bool parent;
    bool fiercing, fin, move;
    int cnt;

    public float speed;

    void Start()
    {
        parent = move = false;
        fiercing = fin = false;
        cnt = 0;
    }

    void Update()
    {
        if (parent && !move)
        {
            c1.transform.localPosition = Vector3.MoveTowards(c1.transform.localPosition,
               new Vector3(-5.46f, 2.68f, -11.92f), 4.0f * Time.deltaTime);
            c2.transform.localPosition = Vector3.MoveTowards(c2.transform.localPosition,
                new Vector3(3, 5.42f, -11.98f), 4.0f * Time.deltaTime);
            c3.transform.localPosition = Vector3.MoveTowards(c3.transform.localPosition,
                new Vector3(4.3f, -2.9f, -11.68f), 4.0f * Time.deltaTime);

            if (c1.transform.localPosition == new Vector3(-5.46f, 2.68f, -11.92f) &&
                c2.transform.localPosition == new Vector3(3, 5.42f, -11.98f) &&
                c3.transform.localPosition == new Vector3(4.3f, -2.9f, -11.68f))
            {
                Invoke("moveTrue", 2.0f);
            }
        }

        if (cnt >= 5)
        {
            fin = true;
        }

        if (move)
        {
            if (!fin && !fiercing)
            {
                c1.transform.localPosition = Vector3.MoveTowards(c1.transform.localPosition,
                new Vector3(-0.52f, -1.11f, -9.92f), speed * Time.deltaTime);
                c2.transform.localPosition = Vector3.MoveTowards(c2.transform.localPosition,
                    new Vector3(-1.1f, 0.43f, -9.75f), speed * Time.deltaTime);
                c3.transform.localPosition = Vector3.MoveTowards(c3.transform.localPosition,
                    new Vector3(0.42f, 1.25f, -10.084f), speed * Time.deltaTime);

                if (c1.transform.localPosition == new Vector3(-0.52f, -1.11f, -9.92f) &&
                    c2.transform.localPosition == new Vector3(-1.1f, 0.43f, -9.75f) &&
                    c3.transform.localPosition == new Vector3(0.42f, 1.25f, -10.084f))
                {
                    fiercing = true;
                }
            }

            if (!fin && fiercing)
            {
                c1.transform.localPosition = Vector3.MoveTowards(c1.transform.localPosition,
                new Vector3(-5.46f, 2.68f, -11.92f), 10.0f * Time.deltaTime);
                c2.transform.localPosition = Vector3.MoveTowards(c2.transform.localPosition,
                    new Vector3(3, 5.42f, -11.98f), 10.0f * Time.deltaTime);
                c3.transform.localPosition = Vector3.MoveTowards(c3.transform.localPosition,
                    new Vector3(4.3f, -2.9f, -11.68f), 10.0f * Time.deltaTime);

                if (c1.transform.localPosition == new Vector3(-5.46f, 2.68f, -11.92f) &&
                    c2.transform.localPosition == new Vector3(3, 5.42f, -11.98f) &&
                    c3.transform.localPosition == new Vector3(4.3f, -2.9f, -11.68f))
                {
                    fiercing = false;
                    cnt += 1;
                }
            }
        }

        if (fin)
        {
            tmp.transform.DetachChildren();

            Init();
        }
    }

    void moveTrue()
    {
        move = true;
    }

    void Init()
    {
        cnt = 0;
        fiercing = move = parent = false;
        fin = false;
    }
}
