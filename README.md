# OpenShift-Ansible-Module
Ansible 2.x module for managing OpenShift

It uses the restful API to create and manage resources, so there is no need to install oc on the server that you are running this from.

The configuration is almost the same as you would find in the yaml spec section of the deployment config and build config.

In most cases it is just to copy and paste what is there directly in to the module.

#### Pre-Requirements:
An authentication token from a high privileged  service account.

Create Service Account:
```
oc project default
oc create serviceaccount ansible
oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible
```
To get the JWT token to authenticate to the API:
```
oc describe serviceaccount ansible
...Find the relevant token...
oc describe secret ansible-token-xxxx
```

#### Example Playbook:
This playbook sets up a complete environment with a hello world application that is fetched from docker-hub.

```yaml
- hosts: localhost
  vars:
    master_url: https://magesticmaster.middleware.se:8443
    auth_token: eydJshsbGciOiJS....
  tasks:
    - name: Project abba
      oscp_project:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976

    - name: Waterloo Imagestream
      oscp_imagestream:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: waterloo

    - name: Chiquitita Service Account
      oscp_serviceaccount:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: chiquitita
        roles:
          - system:image-pusher
          - system:image-puller
          - admin

    - name: Builder Service Account
      oscp_serviceaccount:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: builder
        roles:
          - system:image-pusher

    - name: Deployer Service Account
      oscp_serviceaccount:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: deployer
        roles:
          - admin

    - name: Buildconfig Waterloo
      oscp_buildconfig:
        master_url: "{{ master_url }}"
        auth_token: "{{ auth_token }}"
        name: waterloo-bc
        project: abba1976
        serviceAccount: chiquitita
        triggers:
         - type: ConfigChange
        source:
          type: Dockerfile
          dockerfile: 'FROM mtekkie/hellopython'
          secrets: null
        strategy:
          type: Docker
          dockerStrategy:
            env:
              - name: unused_variable
                value: none
        output:
          to:
            kind: ImageStreamTag
            namespace: abba1976
            name: 'waterloo:latest'

    - name: DeploymentConfig Waterloo-dc.
      oscp_deployconfig:
        master_url: "{{ master_url }}"
        auth_token: "{{ auth_token }}"
        name: waterloo-dc
        project: abba1976
        strategy:
          type: Rolling
          rollingParams:
            updatePeriodSeconds: 1
            intervalSeconds: 1
            timeoutSeconds: 600
            maxUnavailable: 25%
            maxSurge: 25%
          resources: {  }
        triggers:
          - type: ConfigChange
          - type: ImageChange
            imageChangeParams:
              automatic: true
              containerNames:
                - waterloo
              from:
                kind: ImageStreamTag
                name: 'waterloo:latest'
        replicas: 1
        test: false
        selector:
          name: waterloo
        template:
          metadata:
            labels:
              name: waterloo
          spec:
            serviceAccountName: chiquitita
            containers:
              - name: waterloo
                image: '172.30.46.11:5000/abba1976/waterloo'
                ports:
                  - containerPort: 8080
                    protocol: TCP
                resources: {  }
                imagePullPolicy: Always
            restartPolicy: Always
            terminationGracePeriodSeconds: 30
            dnsPolicy: ClusterFirst
            securityContext: {  }

    - name: Waterloo HTTP Service
      oscp_service:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: waterloo-web
        ports:
        - name: http-port
          protocol: TCP
          port: 80
          targetPort: 8080
        selector:
          name: waterloo

    - name: Waterloo inbound route
      oscp_route:
        master_url: "{{ master_url }}"
        auth_token:  "{{ auth_token }}"
        project: abba1976
        name: waterloo-route
        host: waterloo1976.apps.middleware.se
        to:
          kind: Service
          name: waterloo-web
        port:
          targetPort: http-port
        tls:
          termination: edge
          insecureEdgeTerminationPolicy: Redirect
```

Still in development. Known issues:
  - DeploymentConfigurations are always applied everytime. Working on a solution.
