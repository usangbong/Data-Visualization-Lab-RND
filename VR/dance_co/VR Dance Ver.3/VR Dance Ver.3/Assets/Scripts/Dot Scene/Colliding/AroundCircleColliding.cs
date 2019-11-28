using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AroundCircleColliding : MonoBehaviour
{
    AroundCircle ar;
    Vector3 pos;
    bool col, timeCor, timeBool;

    float time;

    private void Start()
    {
        ar = GameObject.Find("AroundCircleManager").GetComponent<AroundCircle>();
        pos = new Vector3(0, 0, 0);
        col = timeCor = timeBool = false;

        time = 0;
    }

    private void Update()
    {
        if (col && !timeBool)
        {
            gameObject.transform.Translate(pos * 5.0f * Time.deltaTime);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (ar.finish)
            {
                pos = diff(gameObject.transform.position, other.gameObject.transform.position);
                col = true;
                int value = RandomValue();
                gameObject.transform.GetComponent<MeshRenderer>().material =
                    ar.matList[value];

                if(!timeCor)
                {
                    StartCoroutine(timeChecker());
                    timeCor = true;
                }
            }
        }
    }

    Vector3 diff(Vector3 pos1, Vector3 pos2)
    {
        Vector3 d;

        d.x = pos1.x - pos2.x;
        d.y = pos1.y - pos2.y;
        d.z = pos1.z - pos2.z;

        return d;
    }

    int RandomValue()
    {
        float num;
        num = Random.value * 1000;

        int n = System.Convert.ToInt32(num) % 8;

        return n;
    }

    IEnumerator timeChecker()
    {
        while(!timeBool)
        {
            time += 0.1f;

            if(time >= 10f)
            {
                timeBool = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}
