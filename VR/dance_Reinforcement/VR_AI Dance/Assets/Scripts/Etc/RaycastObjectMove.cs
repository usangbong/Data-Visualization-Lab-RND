using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RaycastObjectMove : Agent
{
    public GameObject objList;

    RaycastConditionAgent rayAgent;

    bool isObj = true;

    void Awake()
    {
        rayAgent = GameObject.Find("Agent").GetComponent<RaycastConditionAgent>();
    }

    public override void CollectObservations()
    {
        AddVectorObs(isObj);
    }

    public override void AgentAction(float[] vectorAction)
    {
        if(isObj)
        {
            transform.rotation = Quaternion.Euler(RandomRotation());

            RaycastHit hit;
            GameObject selObj = null;

            if(Physics.Raycast(transform.position, transform.forward, out hit, 3f))
            {
                selObj = hit.transform.gameObject;
            }

            if (selObj != null)
            {
                for (var i = 0; i < objList.transform.childCount; i++)
                    if (selObj == objList.transform.GetChild(i).gameObject)
                        rayAgent.raySel = i;
            }

            else rayAgent.raySel = 4;

            isObj = false;

            StartCoroutine(timeChecker());
        }
    }

    Vector3 RandomRotation()
    {
        float x = Mathf.Round(Random.Range(0, 360) * 100f) * 0.01f;
        float y = Mathf.Round(Random.Range(0, 360) * 100f) * 0.01f;
        float z = Mathf.Round(Random.Range(0, 360) * 100f) * 0.01f;

        return new Vector3(x, y, z);
    }

    IEnumerator timeChecker()
    {
        yield return new WaitForSeconds(0.5f);

        isObj = true;
    }
}
