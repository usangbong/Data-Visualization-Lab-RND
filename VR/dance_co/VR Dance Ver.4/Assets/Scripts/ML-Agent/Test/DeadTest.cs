using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class DeadTest : Agent
{
    public float moveForce;
    Vector3 originPos, originRot;
    Rigidbody rigidBody;

    CorWrong cw;

    void Awake()
    {
        rigidBody = GetComponent<Rigidbody>();
        originPos = transform.position;
        originRot = transform.rotation.eulerAngles;

        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();
    }

    public override void AgentReset()
    {
        rigidBody.velocity = Vector3.zero;
        transform.position = originPos;
        transform.rotation = Quaternion.Euler(originRot);
    }

    public override void CollectObservations()
    {
        AddVectorObs(rigidBody.velocity);
        AddVectorObs(transform.position);
    }

    public override void AgentAction(float[] vectorAction)
    {
        rigidBody.AddForce(vectorAction[0] * moveForce, vectorAction[1] * moveForce, vectorAction[2] * moveForce);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "dead")
        {
            Debug.Log(name + " DEAD");
            AddReward(-1f);
            Done();
        }
    }
}
