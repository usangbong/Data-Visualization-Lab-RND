using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeadRaycast : MonoBehaviour
{
    public float moveForce = 10f;

    public float avgVelocity = 0f, sumVelocity;
    int countVelocity = 0;

    public GameObject parentObject;
    List<GameObject> objList = new List<GameObject>();
    public List<float> velList = new List<float>();

    CorWrong cw;

    bool rot = true;
    int rand = 0;

    void Start()
    {
        for(var i=0;i<parentObject.transform.childCount;i++)
        {
            objList.Add(parentObject.transform.GetChild(i).gameObject);
            objList[i].GetComponent<RaycastTest2>().idx = i;
            velList.Add(0);
        }

        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();

        StartCoroutine(timeChecker());
    }

    void Update()
    {
        if (rot)
        {
            Invoke("setRot", 1f);
            rot = false;
        }

        transform.LookAt(objList[rand].transform);

        Debug.DrawRay(transform.position, transform.forward * 5f, Color.red);
        for(var i=0;i<objList.Count;i++)
        {
            objList[i].GetComponent<RaycastTest2>().setHit(false);
        }

        RaycastHit hit;

        if(Physics.Raycast(transform.position, transform.forward, out hit, 5f))
        {
            if(hit.transform.CompareTag("object"))
            {
                hit.transform.GetComponent<RaycastTest2>().setHit(true);
            }
        }

        sumVelocity = 0f;
        for(var i=0;i<objList.Count;i++)
        {
            sumVelocity += velList[i];
        }

        sumVelocity /= objList.Count;
        avgVelocity = avgVelocity + (sumVelocity - avgVelocity) / ++countVelocity;
    }

    IEnumerator timeChecker()
    {
        while (true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;

            for (var i = 0; i < objList.Count; i++)
            {
                objList[i].GetComponent<RaycastTest2>().Done();
            }
        }
    }

    void setRot()
    {
        rand = Random.Range(0, objList.Count);
        rot = true;
    }
}
